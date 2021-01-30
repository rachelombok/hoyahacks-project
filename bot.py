import tweepy
import time
import webbrowser
import config
import csv
import requests
import urllib.request
from news_sources import sources

auth = tweepy.OAuthHandler(config.api_key, config.api_secret_key)
auth.set_access_token(config.access_token, config.access_token_secret)
api = tweepy.API(auth)

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
    tweets = api.mentions_timeline(count=50)
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
        #"{0:.2f}".format(a)
def main():
    replytweets()

main()