#!/usr/bin/python
#  -*- coding: utf-8 -*-

__author__ = 'ommirandap'
import tweepy as tw
import OAuthKeys
import json
from time import sleep


def return_api(n):
    index = n % len(OAuthKeys.credentials)
    keys = OAuthKeys.credentials[index]
    auth = tw.OAuthHandler(keys["CONSUMER_KEY"], keys["CONSUMER_SECRET"])
    auth.secure = True
    auth.set_access_token(keys["ACCESS_TOKEN"], keys["ACCESS_SECRET"])
    return tw.API(auth)


def cleaner(word):
    word = word.replace('"', '').replace('\'', '').replace('\n', ' ').replace("\\", '').replace('\t', ' ').replace('&gt;', '>').replace('&lt;','<')
    word = word.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u").replace("ñ","n")
    word = word.replace("Á", "A").replace("É", "E").replace("Í", "I").replace("Ó", "O").replace("Ú", "U").replace("Ñ", "N")
    #return ''.join([x for x in word if ord(x) < 128])
    return ''.join([x for x in word if True]).encode('utf-8')


def print_tweet(index, tweet):
    date = str(tweet.created_at)
    username = tweet.user.name
    text = cleaner(tweet.text)
    final_text = date + " \t " + username + " \t " + text
    return final_text

n=1
api = return_api(n)
i = 0

with open("/home/ommirandap/PRISMA/DynamicNewsAnalysis/cuentas.txt", 'r') as cuentas:

    for cuenta in cuentas:
        output = open("/home/ommirandap/PRISMA/DynamicNewsAnalysis/data/" + cuenta.replace("\n","") + ".txt", 'w')
        i=0
        for status in tw.Cursor(api.user_timeline, id=cuenta).items(10000):
            i += 1
            jsoniano = json.dumps(status._json)
            output.write(jsoniano + '\n')
            if(i % 1000 == 0):
                print("Llevo " + str(i) + " tweets de la cuenta: " + cuenta + " con credential: " + str(n))
                n += 1
                api = return_api(n)
        print("Duermo un ratito")
        sleep(10*60)


