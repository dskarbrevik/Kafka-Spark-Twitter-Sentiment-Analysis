
#UBS W205 Course Project
#Build Twitter Sentiment Corpus
#The corpus is used as a training dataset for future sentiment analysis

#The implementation is based on the concept from the following paper
#http://cs.stanford.edu/people/alecmgo/papers/TwitterDistantSupervision09.pdf

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from time import time,ctime
import simplejson
import tweepy
import csv

# Define positive and negative emoticons
pos_emoticons = [":)", ":-)", ": )", ":D", "=)"];
neg_emoticons = [":(", ":-(", ": ("];

# Specify key words
keywords = ["hillary", "trump", "presidential election", "politics"]

# Specify OAuth Tokens
consumer_key = "VJyepj171h2jXYEn6hcjQcs2J";
consumer_secret = "caADQ9bQnONquOE6Bx4LupqRNidTwmtGwi4T5j5LpW7Se4YPqJ";
access_token = "792785681022066688-uilRCzaMkh4MkSEhCy5DWExaNpDW8AG";
access_token_secret = "56BYid7nPWU29QUK9yfi7W59a8SpwpqY3iNDCAJpFheiQ";

# Specify run time
duration = 60*60*9

# Check if string is ascii
def ascii_string(s):
  return all(ord(c) < 128 for c in s)

# Extract valid words from Tweet
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

# Twitter Listener Class
class MyTwitterListener(StreamListener):

	def __init__(self,timer):
		self.inc = 0
		StreamListener.__init__(self)
		# report the start of data collection...
		print "Gathering data at %s"%(str(ctime()))
		self.startTime = time()
		print "Start Time = %s"%(str(ctime()))
		self.timer = timer
		self.count = 0

		self.f = open('sentiment_corpus.csv', 'a')
		self.writer = csv.writer(self.f, lineterminator='\n')

	def on_error(self, status):
		print ("ERROR :",status)
		
	def on_data(self, data):
		try:
			self.endTime = time()
			self.elapsedTime = self.endTime - self.startTime
			if self.elapsedTime <= self.timer:
				self.dataJson =simplejson.loads(data[:-1])
				self.dataJsonText = self.dataJson["text"].lower()

				# check if the tweet contains positive or negative emoticons
				positive_emo = False
				negative_emo = False
				if any(emo in self.dataJsonText for emo in pos_emoticons):
					positive_emo = True
				if any(emo in self.dataJsonText for emo in neg_emoticons):
					negative_emo = True				
				if (positive_emo and negative_emo):
					return True
				if (positive_emo==False and negative_emo==False):
					return True
					
				self.count += 1
				print " ".join(s for s in get_valid_words(self.dataJsonText))
				
				# output to file
				if positive_emo:
					self.writer.writerow(['positive', " ".join(s for s in get_valid_words(self.dataJsonText))])
				else:
					self.writer.writerow(['negative', " ".join(s for s in get_valid_words(self.dataJsonText))])
					
				self.f.flush()
				
			else:
				print "Count== ",self.count
				print "End Time = %s"%(str(ctime()))
				print "Elapsed Time = %s"%(str(self.elapsedTime))
				self.f.close()
				return False
			return True
			
		except Exception, e:
			# Catch any unicode errors while printing to console
			# and just ignore them to avoid breaking application.
			pass

if __name__ == '__main__':

	# Create OAuthHandler
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	# Instantiate Twitter Listener
	l = MyTwitterListener(duration)
	mystream = tweepy.Stream(auth, l, timeout=30)
	mystream.filter(languages=["en"], track=keywords, async=False)



