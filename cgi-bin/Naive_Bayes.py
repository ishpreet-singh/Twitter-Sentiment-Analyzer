import argparse
import urllib
import urllib2
import json
import datetime
import sys
import random
import os
import pickle
import oauth2 as oauth
import csv
import re
import string
import time
import nltk.classify
import cgi
import collections
import webbrowser
from datetime import timedelta
from nltk.corpus import stopwords

reload(sys)  
sys.setdefaultencoding('utf8')

form = cgi.FieldStorage()  
keyword = form.getvalue('searchbox')


class Naive_Baise_Classifier:

    def __init__(self):
        self.currDate = datetime.datetime.now()
        self.weekDates = []
        self.weekDates.append(self.currDate.strftime("%Y-%m-%d"))

        for day in range(1,2):
            dateDiff = timedelta(days=-day)
            newDate = self.currDate + dateDiff
            self.weekDates.append(newDate.strftime("%Y-%m-%d"))
 
    
    def getTwitterData(self, keyword, time = 'lastweek'):
        tweets = []
        if(time == 'lastweek'):
            for day in range(0,1):
                params = {'since': self.weekDates[day+1], 'until': self.weekDates[day]}
                currentTweets = self.getData(keyword, params)
                for tweet in currentTweets:
                    #processedTweet, featureVector = self.processTweet(tweet)
                    tweets.append(tweet)
        
        self.filename = 'data/Fetched_Tweets_'+urllib.unquote(keyword.replace("+", " "))+'_'+str(int(random.random()*10000))+'.csv'
        inputFile = open(self.filename, 'wb')
        writer = csv.writer(inputFile)
        writer.writerow(["Tweets"])
        self.tweets = []
        for tweet in tweets:
            processedTweet, featureVector = self.processTweet(tweet)
            writer.writerow([processedTweet])
            self.tweets.append(processedTweet)
        return self.tweets
    
    
    def parseConfig(self):
        config = {}
        if os.path.exists('config.json'):
            with open('config.json') as f:
                config.update(json.load(f))
        else:
          # may be from command line
          parser = argparse.ArgumentParser()

          parser.add_argument('-ck', '--consumer_key', default=None, help='Your developper `Consumer Key`')
          parser.add_argument('-cs', '--consumer_secret', default=None, help='Your developper `Consumer Secret`')
          parser.add_argument('-at', '--access_token', default=None, help='A client `Access Token`')
          parser.add_argument('-ats', '--access_token_secret', default=None, help='A client `Access Token Secret`')

          args_ = parser.parse_args()
          def val(key):
            return config.get(key)\
                   or getattr(args_, key)\
                   or raw_input('Your developper `%s`: ' % key)
          config.update({
            'consumer_key': val('consumer_key'),
            'consumer_secret': val('consumer_secret'),
            'access_token': val('access_token'),
            'access_token_secret': val('access_token_secret'),
          })
        return config
 
    
    def oauthReq(self, url, http_method="GET", post_body=None, http_headers=None):
        config = self.parseConfig()
        consumer = oauth.Consumer(key=config.get('consumer_key'), secret=config.get('consumer_secret'))
        token = oauth.Token(key=config.get('access_token'), secret=config.get('access_token_secret'))
        client = oauth.Client(consumer, token)
 
        resp, content = client.request(
            url,
            method=http_method,
            body=post_body or '',
            headers=http_headers
        )
        return content
 
    
    def getData(self, keyword, params = {}):
        maxTweets = 100
        url = 'https://api.twitter.com/1.1/search/tweets.json?'    
        data = {'q': keyword, 'lang': 'en', 'result_type': 'recent', 'count': maxTweets, 'include_entities': 0}
 
        if params:
            for key, value in params.iteritems():
                data[key] = value
 
        url += urllib.urlencode(data)
        response = self.oauthReq(url)
        jsonData = json.loads(response)
        tweets = []
        if 'errors' in jsonData:
            print "API Error"
            print jsonData['errors']
        else:
            for item in jsonData['statuses']:
                tweets.append(item['text'])            
        return tweets      

    def replaceTwoOrMore(self, s):
        pattern = re.compile(r"(.)\1{1,}", re.DOTALL) 
        return pattern.sub(r"\1\1", s)
    
    def processTweet(self,tweet):
        tweet = tweet.lower()
        #Remove www.* or https?://* 
        tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','',tweet)
        #Remove @username 
        tweet = re.sub('@[^\s]+','',tweet)    
        #Remove additional white spaces
        tweet = re.sub('[\s]+', ' ', tweet)
        tweet = re.sub('rt','',tweet)
        #Replace #word with word
        tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
        #trim
        tweet = tweet.strip('\'"')
        
        #Remove StopWords
        stopWords = stopwords.words('english')
        words = tweet.split()
        featureVector = []
        for w in words:
            #replace two or more with two occurrences 
            w = self.replaceTwoOrMore(w) 
            #strip punctuation
            w = w.strip('\'"?,.')
            #check if it consists of only words
            val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*[a-zA-Z]+[a-zA-Z0-9]*$", w)
            #ignore if it is a stopWord
            if(w in stopWords or val is None):
                continue
            else:
                featureVector.append(w)
        processTweet = ' '.join(featureVector)
        return processTweet,featureVector
    
    
    def extract_features(self, tweet):
        tweet_words = set(tweet)
        features = {}
        for word in self.featureList:
            features['contains(%s)' % word] = (word in tweet_words)
        return features
    
    def train_classifier(self):
        self.featureList = []

        # If data is already trained just Load the classifier
        try:
            f = open('FeatureList.pickle','rb')
            self.featureList = pickle.load(f)

            classifier_training_result = open('classifier_training_result.pickle','rb')
            self.NBClassifier = pickle.load(classifier_training_result)

        except (OSError ,IOError):
            #Else get the training Data 
            inpTweets = csv.reader(open('training_dataset.csv', 'rb'), delimiter=',', quotechar='|')
            tweets = []

            for row in inpTweets:
                sentiment = row[0]
                tweet = row[1]
                processedTweet, featureVector = self.processTweet(tweet)
                self.featureList.extend(featureVector)
                tweets.append((featureVector, sentiment))
            
            self.featureList = list(set(self.featureList))

            # Save FeatureList is a pickle File
            f = open('FeatureList.pickle','wb')
            pickle.dump(self.featureList, f)

            # Generate the training set
            training_set = nltk.classify.util.apply_features(self.extract_features, tweets)
            
            # Train the Naive Bayes classifier
            self.NBClassifier = nltk.NaiveBayesClassifier.train(training_set)

            # Save the result from classifier in  a pickle File
            classifier_training_result = open('classifier_training_result.pickle','wb')
            pickle.dump(self.NBClassifier, classifier_training_result)
            #print nltk.classify.accuracy(NBClassifier, training_set)
            #Accuracy of this program is 0.9012

    def test_classifier(self, test_tweets):
        sentiments = []
        testTweets = []
        self.filename=(self.filename).replace(self.filename[:5],'')
        outputFile = open('data/Output_'+self.filename,"wb")
        writer = csv.writer(outputFile)
        writer.writerow(["Tweet","Sentiment"])
        
        for test_tweet in test_tweets:
            testTweets.append(test_tweet)
            processedTweet, featureVector = self.processTweet(test_tweet)
            sentiment = self.NBClassifier.classify(self.extract_features(featureVector))
            sentiments.append(sentiment)
            
        for tweet in range(0,len(testTweets)):
            writer.writerow([testTweets[tweet],sentiments[tweet]])

        result = collections.Counter(sentiments)
        resultFile = 'data/Result_'+self.filename
        resFile = open(resultFile, 'wb')
        writer = csv.writer(resFile)
        writer.writerow(['TotalTweets',len(sentiments)])
        for key, value in result.items():
            key = key.replace('"','')
            writer.writerow([key, value])

#Find Tweets and Sentiments for the given keyword
def Sentiment_Analyzer():
    obj = Naive_Baise_Classifier()
    tweets = obj.getTwitterData(keyword)
    obj.train_classifier()
    obj.test_classifier(tweets)
    
if __name__ == '__main__':
    Sentiment_Analyzer()
    url="http://localhost/search_result_1.php?data="+cgi.FieldStorage().getvalue('searchbox')
    webbrowser.open(url,new=0, autoraise=True)