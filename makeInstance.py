#!/usr/bin/env python2
#coding:utf-8

import time
import twitter
import keys


def twApi(accountName = None):
    if (accountName == None):
        return twitter.Api(
            consumer_key = keys.accountKeys['consumer_key'],
            consumer_secret = keys.accountKeys['consumer_secret'],
            access_token_key = keys.accountKeys['access_token_key'],
            access_token_secret = keys.accountKeys['access_token_secret'])
    else:
        if (accountName in keys.accountDic):
            return twitter.Api(
                consumer_key = keys.accountDic[accountName]['consumer_key'],
                consumer_secret = keys.accountDic[accountName]['consumer_secret'],
                access_token_key = keys.accountDic[accountName]['access_token_key'],
                access_token_secret = keys.accountDic[accountName]['access_token_secret'])
        else:
            print 'Error in makeInstance'

if __name__ == '__main__':
    # api = twApi()
    api = twApi('vehcdra')
    rate = api.GetRateLimitStatus()
    print "home_timeline Limit: %d/%d" % (rate['resources']['statuses']['/statuses/home_timeline']['remaining'],rate['resources']['statuses']['/statuses/home_timeline']['limit'])
    tm = time.localtime(rate['resources']['statuses']['/statuses/home_timeline']['reset'])
    print "home_timeline Reset Time: %d:%d" % (tm.tm_hour , tm.tm_min)

    print "user_timeline Limit: %d/%d" % (rate['resources']['statuses']['/statuses/user_timeline']['remaining'],rate['resources']['statuses']['/statuses/user_timeline']['limit'])
    tm = time.localtime(rate['resources']['statuses']['/statuses/user_timeline']['reset'])
    print "user_timeline Reset Time: %d:%d" % (tm.tm_hour , tm.tm_min)
