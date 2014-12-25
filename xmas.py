#!/usr/bin/env python2
#coding:utf-8

import twitter
import keys
import makeInstance as tw
import datetime

def setTime(tstr):
    timeList = tstr.split(' ')
    # UTCオフセットを含む処理が上手くいかなかったので，とりあえずトリミングしとく
    timeList.pop(4)
    trimDateStr = ''.join(timeList)
    tdatetime = datetime.datetime.strptime(trimDateStr, '%a%b%d%H:%M:%S%Y')
    return tdatetime


def trimTweet(tweet):
    trimTweetData = {
        'userID' : tweet.user.id,
        'screenName' : tweet.user.screen_name,
        'tweetID' : tweet.id,
        'tweetTime' : setTime(tweet.created_at),
        'favorited' : tweet.favorited,
        'text' : tweet.text
    }
    return trimTweetData


def getTargetUsersTweet(api, user, num):
    maxId = None
    counter = 0

    if 200 < num:
        maxNum = num
        num = 200

    tweetList = []
    while (counter <= maxNum):
        timeline = api.GetUserTimeline(screen_name = user, count = num, max_id = maxId)
        maxId = timeline[len(timeline)-1].id
        for tweet in timeline:
            if tweet.retweeted_status is None: # remove retweet
                tweetList.append(trimTweet(tweet))
        counter += num
    print 'tweetList len: ', len(tweetList)
    return tweetList


def favorite(api, tweet):
    if tweet['favorited'] == False:
        api.CreateFavorite(id = tweet['tweetID'])


xmasStart = datetime.datetime(year = 2014, month = 12, day = 24, hour = 21, minute = 0)
xmasEnd   = datetime.datetime(year = 2014, month = 12, day = 25, hour = 5, minute = 0)


def checkTweet(twList):
    xmasTweetNum = 0
    dateDict = {}
    for tweet in twList:
        # クリスマス前かつそれっぽい時間
        if tweet['tweetTime'] < xmasStart and (xmasStart.time() < tweet['tweetTime'].time() < datetime.time.max or datetime.time.min < tweet['tweetTime'].time() < xmasEnd.time()):
            if tweet['tweetTime'].strftime('%Y%m%d') in dateDict:
                dateDict[tweet['tweetTime'].strftime('%Y%m%d')] += 1
            else:
                dateDict[tweet['tweetTime'].strftime('%Y%m%d')] = 1

        if xmasStart < tweet['tweetTime'] < xmasEnd:
            xmasTweetNum += 1

    dailyTweetNum = 0.
    for num in dateDict.values():
        dailyTweetNum += num
    averageTweetNum = dailyTweetNum/len(dateDict)
    print xmasTweetNum, '/', averageTweetNum
    if xmasTweetNum < averageTweetNum:
        return True
    else:
        return False

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print "Please input a screen_name of target account．"
        sys.exit()
    botApi = tw.twApi()
    twList = getTargetUsersTweet(api = botApi, user = sys.argv[1], num = 1000)
    if checkTweet(twList):
        print sys.argv[1], 'must die.'
    else:
        print sys.argv[1], 'is a friend.'
