#!/usr/bin/env python2
#coding:utf-8

import datetime
import twitter
import keys
import makeInstance as tw


def trimTweet(tweet):
    trimTweetData = {
        'tweetID' : tweet.id,
        'userID' : tweet.user.id,
        'screenName' : tweet.user.screen_name,
        'favorited' : tweet.favorited,
        'text' : tweet.text
    }
    return trimTweetData


def getTargetUsersTweet(api, user, num = 200):
    timeline = api.GetUserTimeline(screen_name = user, count = num)
    tweetList = []
    for tweet in timeline:
        if tweet.retweeted_status is None: # remove retweet
            tweetList.append(trimTweet(tweet))
    return tweetList


def favorite(api, tweet):
    if tweet['favorited'] == False:
        api.CreateFavorite(id = tweet['tweetID'])


if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print "Please input a screen_name of target account．"
        sys.exit()
    api = tw.twApi()
    twList = getTargetUsersTweet(api=api, user=sys.argv[1])
    for tw in twList:
        favorite(api, tw)
        print tw['text']
