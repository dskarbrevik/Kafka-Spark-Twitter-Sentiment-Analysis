
#UBS W205 Course Project
#Sentiment Analysis
#Pyspark program that performs sentiment analysis of Twitter data

# Install pip3 on Redhat
#$ sudo yum install python34-setuptools
#$ sudo easy_install-3.4 pip

# Install nltk and numpy lib
#$sudo pip3 install -U nltk
#$sudo pip3 install -U numpy

# Run spark-submit with python 3.4
#PYSPARK_PYTHON=python3.4 /data/spark15/bin/spark-submit sentiment_analysis.py

from pyspark import SparkContext, SparkConf
from pyspark.sql import HiveContext
import nltk
import csv
import sys
import subprocess

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
		
conf = SparkConf().setAppName("sentiment_analysis").setMaster("local")
sc = SparkContext(conf=conf)
hive_context = HiveContext(sc)

sentiment_corpus = load_sentiment_corpus()	
word_features = get_word_features(get_words_in_tweets(sentiment_corpus))
print ('word features: ', len(word_features))

#training_set = nltk.classify.apply_features(extract_features(word_features), tweets)
# Create Training Set based on features
training_set = [(extract_features(d), c) for (d,c) in sentiment_corpus]
print ('training set: ', len(training_set))

# Train NB classifier
classifier = nltk.NaiveBayesClassifier.train(training_set)
classifier.show_most_informative_features(10)

# Test NB classifier
#tweet = 'i am lying hillarys'
#print (classifier.classify(extract_features(tweet.split())))
#print (tweet)

# retrieve data from Hive tables
twitter_table = hive_context.table("twitter.twitter_structured_data")
#twitter_table.show()
twitter_table.registerTempTable("twitter_structured_data")
twitter_rows = hive_context.sql("select * from twitter_structured_data where (length(text) > 0)")

# run classify
r = twitter_rows.map(lambda p: [p.topic, p.text, p.created_at_dt, p.batchid])


try:
	f = open('sentiment_output.csv', 'w')
	writer = csv.writer(f)
	result = []
	for t in r.collect():
		topic = t[0]
		tweet = t[1]
		created_at_dt = t[2]
		valid_words = get_valid_words(tweet)
		sentiment = 'positive'
		sentiment = classifier.classify(extract_features(valid_words))
		print(topic, ":", sentiment, ":", created_at_dt, ":", valid_words)
		#result.append([topic, sentiment, created_at_dt, t[3]])
		writer.writerow([topic, sentiment, created_at_dt, t[3]])	
finally:
	f.close()

# Append file to HDFS
#hdfs dfs -appendToFile sentiment_output.csv /user/w205/twitter/twitter_result/sentiment_output.csv
p = subprocess.Popen('hdfs dfs -appendToFile sentiment_output.csv /user/w205/twitter/twitter_result/sentiment_output.csv', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
for line in p.stdout.readlines():
    print (line)
retval = p.wait()

# export back to HDFS
#output = sc.parallelize(result)
#output = output.map(lambda x: ','.join(str(d) for d in x))
#output.saveAsTextFile('hdfs://localhost/user/w205/twitter/twitter_result')



