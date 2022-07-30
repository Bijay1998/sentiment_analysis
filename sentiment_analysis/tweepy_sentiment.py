from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
from datetime import datetime, date, time, timedelta
from collections import Counter

import tweepy

import pandas as pd

class Import_tweet_sentiment:

	consumer_key="szxzozHgdCTceW5Ejgo5IEnze"
	consumer_secret="2VozKKOPyBej5QBYToikeF2fo5WABVgMULLT0sttwlXuKThgHA"
	access_token="1515662160067661824-cF4r7bBxym2EOJ5AR5nuaX5Ht3ZYJ8"
	access_token_secret="6ZbfmIts5tPLNkws6X1YlcaYcxZK6P8Fin95sU4RCnkL3"

	#converting tweets to dataframe
	def tweet_to_data_frame(self, tweets):
		df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])
		return df

	#getting the tweets
	def get_tweets(self, handle):
		auth = OAuthHandler(self.consumer_key, self.consumer_secret)
		auth.set_access_token(self.access_token, self.access_token_secret)
		auth_api = API(auth)

		account = handle
		item = auth_api.user_timeline(id=account,count=20)
		df = self.tweet_to_data_frame(item)

		all_tweets = []
		for j in range(20):
			all_tweets.append(df.loc[j]['Tweets'])
		return all_tweets

	def get_hashtag(self, hashtag):
		#creating authentication object
		auth = OAuthHandler(self.consumer_key, self.consumer_secret)
		#setting access token
		auth.set_access_token(self.access_token, self.access_token_secret)
		#creating api object
		auth_api = API(auth)
		
		#creating a list to store tweets
		account = hashtag
		all_tweets = []

		#getting tweets upto 10 tweets
		for tweet in tweepy.Cursor(auth_api.search_tweets, q=account, lang='en').items(10):
			all_tweets.append(tweet.text)

		return all_tweets
