# -*- coding: utf-8 -*-
"""
Small script created to search tweets by keywords, with the aim of informing passengers of their rights as an airline customer.
No Contestar: list of usernames which should not be answered
Userlist: list of usernames which have already been answered.
Created on Tue May 29 17:12:46 2018
"""

#Importamos librerías

import sys
import os

project_root = os.path.abspath(os.path.join(os.getcwd(), '..', '..'))
src_root = os.path.abspath(os.path.join(os.getcwd(), '.', '..'))

sys.path.append(project_root)  # add to the path the project root
sys.path.append(src_root)

import json
import tweepy
import datetime
import time
import pandas as pd
from collections import OrderedDict
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

NOT_RESPONDING = 'API NOT RESPONDING FOR 20 MINUTES'
INCORRECT_DATE_FORMAT = "Incorrect date format, should be YYYY-MM-DD"

# The authentication credentials are obtained from developer.twitter.com/en/apps

consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")
access_key = os.environ.get("ACCESS_KEY")
access_secret = os.environ.get("ACCESS_SECRET")

# Set up your authorizations
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)

# Set up API call
api = tweepy.API(auth, parser = tweepy.parsers.JSONParser())

# VADER API init
analyzer = SentimentIntensityAnalyzer()

# Keywords
keywords1 = ['retraso ryanair', 'cancelación ryanair', 'retrasan ryanair', 'cancelan ryanair', 'retrasos ryanair', 'cancelaciones ryanair']
keywords2 = ['retraso vueling', 'cancelación vueling','retrasan vueling', 'cancelan vueling', 'retrasos vueling', 'cancelaciones vueling']
keywords3 = ['retraso iberia', 'cancelación iberia','retrasan iberia', 'cancelan iberia', 'retrasos iberia', 'cancelaciones iberia']
keywords4 = ['retraso air europa', 'cancelación air europa', 'retraso aireuropa', 'cancelación aireuropa','retrasos aireuropa', 'cancelaciones aireuropa','retrasos air europa', 'cancelaciones air europa']
keywords5 = ['retraso air france', 'cancelación air france', 'retraso airfrance', 'cancelación air france','retrasos airfrance', 'cancelaciones airfrance', 'retrasos air france', 'cancelaciones air france']
keywords6 = ['retraso norwegian', 'cancelación norwegian','retraso easyjet', 'cancelación easyjet','retrasos norwegian', 'cancelaciones norwegian','retrasos easyjet', 'cancelaciones easyjet']
keywords7 = ['retraso klm', 'cancelación klm', 'retraso lufthansa', 'cancelación lufthansa', 'retrasos klm', 'cancelaciones klm', 'retrasos lufthansa', 'cancelaciones lufthansa']
keywords8 = ['retraso iberia express', 'cancelación iberia express', 'retraso british airways', 'cancelación british airways', 'retraso iberiaexpress', 'cancelación ibreriaexpress','retraso britishairways', 'cancelación britishairways']

Tweet_List = []
Tweets_DF = []
waitTime = 0

# Creating the function to get Tweets

def getTweetsDF(numberOfTweets, language, searchQuery, since='since', until='until', idlast = None): #date usage example: '2017-08-22'
    global Tweet_List
    # searchQuery += ' -filter:retweets -since:2017-09-01 -until:2017-09-19'
    if (since != 'since' or until != 'until'):
        try:
              datetime.datetime.strptime(since, '%Y-%m-%d')
              datetime.datetime.strptime(until, '%Y-%m-%d')
              searchQuery += ' since:'+since+' until:'+until
              print(searchQuery + ' is the searchQuery')
        except ValueError:
              return INCORRECT_DATE_FORMAT
    tweet_count = 0 
    
    while (tweet_count <= numberOfTweets):
          print (tweet_count)
          try:
                if(tweet_count == 0):
                      data = api.search(q = searchQuery, count = 5, lang = language , result_type = 'recent', max_id = idlast)
                # tweet list is stored in index 0. [0][2] means second tweet of the list.                          
                else: 
                      data = api.search(q = searchQuery, count = 5, lang = language , result_type = 'recent', max_id = last_id)
                waitTime = 0
          except tweepy.TweepError:
                if (waitTime > 60 * 5): # If API is not responding for more than 5 mins
                      return NOT_RESPONDING
                print('Rate Limit Error. Waiting for 60 seconds...')
                time.sleep(60)
                waitTime += 60
                continue
          data = list(data.values())[0]
          if len(data) < 2:
                print ('Data is empty')
                break
          last_id = data[-1]['id']
          itemcount = len(data)
          print ('item count: '+ str(itemcount))
          Tweet_List += data
          tweet_count =tweet_count + int(itemcount) 
          time.sleep(0.2)
    Tweets_DF = pd.DataFrame(Tweet_List)
    return Tweets_DF
#%%
# Second part 
    
try:
    
    with open('No_Contestar.txt') as f:
		# We dont want to answer the following twitter accounts
        No_Contestar = f.readlines()
        No_Contestar = [user.rstrip() for user in No_Contestar]
        
    with open('userlist.txt') as f:
        userlist = f.readlines()
        userlist = [user.rstrip() for user in userlist]
    

except Exception as e:
    print('Probably the file is not created: ' + str(e))
    

def replyUsers(dataframe):
    print('Replying to the tweets...')
    for index, row in dataframe.iterrows():
        username = row['user']['screen_name']
        tweetID = row['id']
        if username not in No_Contestar:
            if username not in userlist:
                userlist.append(username)
                api.update_status('@'+username+ ' ¿Incidencias en su vuelo? Compruebe si tiene derecho a una compensación. Podemos ayudarle. https://goo.gl/q1tmqC', in_reply_to_status_id=tweetID)
                with open ('userlist.txt', 'a') as userlistfile:
                    userlistfile.write(username+'\n')
                    userlistfile.close()
                    with open ('userlist.txt') as f:
                        userlist = f.readlines()
                        longitud = len(userlist)
                        if longitud>500:
                            x = userlist[0]
                            f.close()
                            f = open('userlist.txt', 'w')
                            for user in userlist:
                                if user != x:
                                    f.write(user)
                                    f.close()

import time

while True:
# Checking keyword by keyword
    for keyword in keywords1, keywords2, keywords3, keywords4, keywords5, keywords6, keywords7, keywords8:
        query = keyword + ' -filter:retweets'
        tweets = getTweetsDF(5, 'es', query) 
        replyUsers(tweets)
    print('Collected all tweets. Waiting for 120 minutes...')
    time.sleep(60*120)