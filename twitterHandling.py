#!/usr/bin/python2.7
# file: twitterHandling.py
# Eilidh Southren - 1513195


#-----------------------------------
#
#       This script sends a tweet to
#       the user if they have supplied
#       authorisation credentials in a 
#       text file.
#



import tweepy
import time
import os.path

# read twitter_credentials text file, if the file exists

if os.path.isfile('twitter_credentials.txt'):

        with open("twitter_credentials.txt") as file:
            line = file.readlines()

        # set authentication variables and strip \n characters 
        api_token = line[0].rstrip('\n')
        api_secret = line[1].rstrip('\n')
        access_token = line[2].rstrip('\n')
        access_token_secret = line[3].rstrip('\n')

        auth= tweepy.OAuthHandler(api_token, api_secret)
        auth.set_access_token(access_token, access_token_secret)

        api = tweepy.API(auth)

        currentTime = time.strftime("%d/%m/%y - %H:%M:%S")

        # update status

        api.update_status("RasProtect Alarm System Triggered: " + currentTime)

else:
        print("Twitter Credentials have not been supplied, twitter notification not sent."
