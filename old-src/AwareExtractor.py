#!/usr/bin/python
#  -*- coding: utf-8 -*-

__author__ = 'ommirandap'
import json

import tweepy as tw

import OAuthKeys


def return_api(n):
    index = n % len(OAuthKeys.credentials)
    keys = OAuthKeys.credentials[index]
    auth = tw.OAuthHandler(keys["CONSUMER_KEY"], keys["CONSUMER_SECRET"])
    auth.secure = True
    auth.set_access_token(keys["ACCESS_TOKEN"], keys["ACCESS_SECRET"])
    return tw.API(auth)


def main():
    CUENTA = "ommirandap"
    index = 0
    api = return_api(index)

    output = open("/home/ommirandap/PRISMA/dynews/" + CUENTA + "-page.txt", 'w')

    lastID = ""
    n_tweets = 0
    n_requests = 0

    while n_tweets <= 4000:
        if (n_requests % 20 == 0):
            index += 1
            api = return_api(index)

        print("Llevo %d tweets con %d credenciales" % (n_tweets, n_requests))

        if lastID == "":
            print lastID
            for statusCollection in tw.Cursor(api.user_timeline, id=CUENTA).pages(1):
                n_requests += 1
                n_tweets += 20
                for status in statusCollection:
                    to_json = json.dumps(status._json)
                    output.write(to_json + "\n")
                    print str(status._json["id_str"])
                    lastID = status._json["id_str"]
        else:
            print lastID
            #for statusCollection in tw.Cursor(api.user_timeline, id=CUENTA, max_id=lastID).pages(1):
            for status in api.user_timeline(id=CUENTA, max_id=lastID, count=20):
                n_requests += 1
                n_tweets += 1
                #for status in statusCollection:
                to_json = json.dumps(status._json)
                output.write(to_json + "\n")
                print str(status._json["id_str"])
                lastID = status._json["id_str"]

if __name__ == "__main__":
        main()