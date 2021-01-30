import tweepy
import time
#import webbrowser
import config
#import csv
import requests
import urllib.request
from news_sources import sources
from os import environ

CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACCESS_KEY = environ['ACCESS_KEY']
ACCESS_SECRET = environ['ACCESS_SECRET']

auth = tweepy.OAuthHandler(config.api_key, config.api_secret_key)
auth.set_access_token(config.access_token, config.access_token_secret)
api = tweepy.API(auth)

INTERVAL = 60 * 60 * 2 # checks mentioned every 2 hours

def bias_measure(percentage, slant):
    if percentage <= 14:
        return "\nNeutral/Balanced"
    elif (percentage > 14 & percentage <= 43):
        return "\nSkews" + slant
    elif (percentage > 43 & percentage <= 71):
        return "\nHyper Partisan" + slant
    elif (percentage > 71):
        return "\nMost Extreme" + slant

def replytweets():
    latest_mention = api.mentions_timeline(count=1)
    mostRecentid = latest_mention[0].id
    tweets = api.mentions_timeline(since_id = mostRecentid, count=10)
    for tweet in tweets:
        print(tweet.text)
        print(tweet.in_reply_to_user_id)
        print(tweet.is_quote_status)

        if (tweet.is_quote_status):
            # if this tweet is a quote of a news source
            print('qupye')
            op_tweet = api.get_status(tweet.quoted_status_id)
            op_user = op_tweet.user.screen_name
            print(op_user)
            if op_user in sources:
                reliability = (sources[op_user][1] / 64) * 100
                bias = (sources[op_user][2] / 42) * 100
                slant = ' Right'
                if bias < 0:
                    slant = ' Left'
                    bias *= -1
                lean = bias_measure(int(bias), slant)
                newtweet = "Publication: " + sources[op_user][0] + "\nSource Reliability: " + str("{0:.2f}".format(reliability)) + "%\n" + "Bias: " + str("{0:.2f}".format(bias)) + "%" + slant + lean
            else:
                newtweet = "This news source is not yet covered."
            print(newtweet)
            api.update_status('@' + tweet.user.screen_name + ' ' + newtweet, tweet.id)

        else:
            # or if tweet is a reply, find OP
            if (tweet.in_reply_to_status_id):
                op_tweet = api.get_status(tweet.in_reply_to_status_id)
                print('here', op_tweet.in_reply_to_status_id_str)

                while (op_tweet.in_reply_to_status_id_str != None):
                    op_tweet = api.get_status(op_tweet.in_reply_to_status_id)
                    

                op_user = op_tweet.user.screen_name
                if op_user in sources:
                    reliability = (sources[op_user][1] / 64) * 100
                    bias = (sources[op_user][2] / 42) * 100
                    slant = ' Right'
                    if bias < 0:
                        slant = ' Left'
                        bias *= -1
                    lean = bias_measure(int(bias), slant)
                    newtweet = "Publication: " + sources[op_user][0] + "\nSource Reliability: " + str("{0:.2f}".format(reliability)) + "%\n" + "Bias: " + str("{0:.2f}".format(bias)) + "%" + slant + lean
                else:
                    newtweet = "This news source is not yet covered."
                print(newtweet)
                api.update_status('@' + tweet.user.screen_name + ' ' + newtweet, tweet.id)
        # mostRecentid = api.mentions_timeline(since_id=mostRecentid, count=1)
        mostRecentid = tweet.id
        #"{0:.2f}".format(a)

#Query Search Function
#define or search for relevant tweets based on the topic, and from a specified twitter handle
#reply to the tweet with the most relevant article from that handle, including its credibility status.
#example: @hoyabot topic: Proud Boys @cnnbrk
def query_search():
    tweets = api.mentions_timeline(count=10)
    newtweet = ""
    for tweet in tweets:
        #command only runs if user presents topic: in their tweet to the bot.
        query = tweet.text.split()
        if (query[1] == "topic:"):
            subject = ""
            #builds the subject, or topic, the user presents to the bot
            for i in range(2,len(query)-1):
                subject += query[i] + " "
            handle = query[len(query)-1].replace("@", "") #the news source is the last thing in tweet (if done properly)
            for source in api.search(q=subject, lang="en", result_type="popular", count=100):
                if (source.author.screen_name == handle): #tries to find the matching source and article
                    if handle in sources: #same code as before, rates the credibility and replies back.
                        reliability = (sources[handle][1] / 64) * 100
                        bias = (sources[handle][2] / 42) * 100
                        slant = ' Right'
                        if bias < 0:
                            slant = ' Left'
                            bias *= -1
                        lean = bias_measure(int(bias), slant)
                        newtweet = "Article: " + source.text + "\nPublication: " + sources[handle][0] + "\nSource Reliability: " + str("{0:.2f}".format(reliability)) + "%\n" + "Bias: " + str("{0:.2f}".format(bias)) + "%" + slant + lean
                    else:
                        newtweet = "This news source is not yet covered."
                    print(newtweet)
                    api.update_status('@' + tweet.user.screen_name + ' ' + newtweet)
# end query_search

def main():
    #replytweets()
    query_search()
    time.sleep(INTERVAL)

main()
