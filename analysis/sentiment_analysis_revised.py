
#UBS W205 Course Project
#Sentiment Analysis
#Pyspark program that performs sentiment analysis of Twitter data
#Created By: Shuang Chan, David Skarbrevik
#Created On: 11/01/2016
#Target Environment: HIVE, PYSPARK, PYTHON 3.4

# Install pip3 on Redhat
#$sudo yum install python34-setuptools
#$sudo easy_install-3.4 pip

# Install nltk and numpy lib
#$sudo pip3 install -U nltk
#$sudo pip3 install -U numpy

# Run spark-submit with python 3.4
# PYSPARK_PYTHON=python3.4 /data/spark15/bin/spark-submit sentiment_analysis_revised.py

from pyspark import SparkContext, SparkConf
from pyspark.sql import HiveContext

import nltk
import csv
import simplejson
import string
import sys
import time
import datetime

month_dict = {"Jan" : "01", 
              "Feb" : "02",
              "Mar" : "03",
              "Apr" : "04",
              "May" : "05",
              "Jun" : "06",
              "Jul" : "07",
              "Aug" : "08",
              "Sep" : "09",
              "Oct" : "10",
              "Nov" : "11",
              "Dec" : "12"}
			  
def ascii_string(s):
  return all(ord(c) < 128 for c in s)

def get_valid_words(tweet):

    words = tweet.split()
	
	# Filter out the hash tags, RT, @ and urls
    valid_words = []
    for word in words:
        # Filter the hash tags
        if word.startswith("#"): continue
        # Filter the user mentions
        if word.startswith("@"): continue
        # Filter out retweet tags
        if word.startswith("rt"): continue
        # Filter out the urls
        if word.startswith("http"): continue
        # Filter the html string
        if word.startswith("&"): continue		
        # Strip leading and lagging punctuations
        aword = word.strip("\"?!><,\'\.:;()-")
        # now check if the word contains only ascii
        if len(aword) >= 3 and ascii_string(aword):
            valid_words.append(aword)
			
    return valid_words
		
def load_sentiment_corpus():
	sentiment_corpus_dict = {}
	f = open('sentiment_corpus.csv', 'r', encoding='utf-8')
	try:
		reader = csv.reader(f)
		for row in reader:
			if (len(row[1])>0 and ascii_string(row[1])):
				sentiment_corpus_dict.update({row[1] : row[0]})
	finally:
		f.close()
		
	#sentiment_corpus = list(set(sentiment_corpus))
	sentiment_corpus = []
	for key, value in sentiment_corpus_dict.items():
		temp = [key.split(),value]
		sentiment_corpus.append(temp)
		
	print ('sentiment corpus: ', len(sentiment_corpus))
	return (sentiment_corpus)

def get_words_in_tweets(tweets):
    all_words = []
    for (words, sentiment) in tweets:
      all_words.extend(words)
    return all_words

def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
    return word_features

def extract_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['c(%s)' % word] = (word in document_words)
    return features
		

# init Spark environment
print ('initializing SPARK environment...')
conf = SparkConf().setAppName("sentiment_analysis").setMaster("local")
sc = SparkContext(conf=conf)
sc.setLogLevel("ERROR")

hive_context = HiveContext(sc)
hive_context.setConf("hive.exec.dynamic.partition.mode", "nonstrict")
hive_context.setConf("hive.exec.dynamic.partition", "true")
hive_context.setConf("hive.mapred.supports.subdirectories", "true")
hive_context.setConf("mapred.input.dir.recursive", "true")

# load training data
print ('loading training data...')
sentiment_corpus = load_sentiment_corpus()	
word_features = get_word_features(get_words_in_tweets(sentiment_corpus))
training_set = [(extract_features(d), c) for (d,c) in sentiment_corpus]
print ('training set: ', len(training_set), ' word features: ', len(word_features))

# Train NB classifier
print ('building model...')
classifier = nltk.NaiveBayesClassifier.train(training_set)
classifier.show_most_informative_features(10)

# Register Hive tables
print ('registering HIVE tables...')
twitter_raw_json = hive_context.table("twitter.twitter_raw_json")
twitter_raw_json.registerTempTable("twitter_raw_json")
twitter_result = hive_context.table("twitter.twitter_result")
twitter_result.registerTempTable("twitter_result")

lastnum = 0
batchsize = 200
startTime = datetime.datetime.now()
endtime = datetime.datetime.now()
duration = 3600

while ((endtime - startTime).seconds <= duration):

	# Retrieve Twitter Raw JSON
	print ("fetching data...%s-%s" % (lastnum+1, lastnum+batchsize))
	twitter_select = hive_context.sql("select * from (select topic, json_response, row_number() over() as rnum from twitter_raw_json)x where x.rnum > %s and x.rnum <= %s" % (lastnum, lastnum+batchsize))
	twitter_rows = twitter_select.map(lambda p: [p.topic, p.json_response])

	try:
		count = 0
		for t in twitter_rows.collect():
		
			count = count + 1
			lastnum = lastnum + 1
			topic = t[0]
			
			try:
				# load json object and extract text and create_at timestamp
				tweetJSON = simplejson.loads(t[1])
				tweet = tweetJSON["text"].lower()
				created_at_dt = tweetJSON["created_at"]

				# parse create timestamp
				year = created_at_dt[26:30]
				month = month_dict[created_at_dt[4:7]]
				day = created_at_dt[8:10]
				timestr = created_at_dt[11:19]
				datetimestr = year + '-' + month + '-' + day + ' ' + timestr
				datestr = year + '-' + month + '-' + day
				
				# extract valid words
				valid_words = get_valid_words(tweet)
				
				# run classifier to determine sentiment
				sentiment = classifier.classify(extract_features(valid_words))
				insertstr = "select '" + topic + "' as topic, '" + sentiment \
							+ "' as sentiment, '" + datetimestr + "' as created_at_dt, '" \
							+ " ".join(s.replace('\'', '') for s in valid_words) + "' as valid_words, '" \
							+ datestr + "' as xdate"
				
			except:
				#print ('Bad Format: %s' % t[1])
				continue
			
			#print (insertstr)
			
			#Combine DataFrame
			if (count > 1):
				df = df.unionAll(hive_context.sql(insertstr))
			else:
				df = hive_context.sql(insertstr)

		# Write DataFrame to HIVE Table
		if (count > 0):
			df.write.mode("append").partitionBy("xdate").saveAsTable("twitter_result")
		
		if (count < batchsize):
			print("waiting for new data...")
			time.sleep(10)
			
	finally:
		endtime = datetime.datetime.now()




