#!/usr/bin/python
#  -*- coding: utf-8 -*-

__author__ = 'ommirandap'
import tweepy as tw
import OAuthKeys
import json
from kitchen.text.converters import to_unicode, to_bytes
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

n=0
api = return_api(n)
i = 0

#output_file = codecs.open("/home/ommirandap/PRISMA/DynamicNewsAnalysis/" + cuenta + ".txt", 'w+', 'utf-8')

#with open("/home/ommirandap/PRISMA/DynamicNewsAnalysis/cuentas.txt", 'r') as cuentas:

output = open("/home/ommirandap/PRISMA/DynamicNewsAnalysis/output_kitchen.txt", 'w')

cuenta = "lun"
for status in tw.Cursor(api.user_timeline, id=cuenta).items(10000):
    i += 1
    #output.write(to_bytes(print_tweet(i, status)) + '\n')
    #print(str(print_tweet(i, status)))
    jsoniano = json.dumps(status._json)
    output.write(jsoniano + '\n')
    #print(jsoniano)
    #print jsoniano.get("text")

    if(i==1000):
        i=0
        n=n+1
        api = return_api(n)
    #sleep(2)
    #break


