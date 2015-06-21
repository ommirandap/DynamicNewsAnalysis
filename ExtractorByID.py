#!/usr/bin/python
#  -*- coding: utf-8 -*-

__author__ = 'ommirandap'
import tweepy as tw
import OAuthKeys
import json, os, sys
from time import sleep

# Global variables
TW_ACCOUNT = LAST_ID = ""
CURRENT_DIR = DATA_DIR = RAW_DATA_DIR = PROC_DATA_DIR = ""
inputfile = None


def setup():
	global TW_ACCOUNT, LAST_ID
	sizeVar = len(sys.argv)

	if(sizeVar == 2):
		TW_ACCOUNT = sys.argv[1]
	elif(sizeVar == 3):
		TW_ACCOUNT = sys.argv[1]
		LAST_ID = sys.argv[2]
	else:
		print("Bad Args")
		exit()

	global CURRENT_DIR, DATA_DIR, RAW_DATA_DIR, PROC_DATA_DIR
	CURRENT_DIR = os.getcwd()
	DATA_DIR = os.path.join(CURRENT_DIR, "data")
	RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
	PROC_DATA_DIR = os.path.join(DATA_DIR, "processed")


def returnAPI(n):
    index = n % len(OAuthKeys.credentials)
    keys = OAuthKeys.credentials[index]
    auth = tw.OAuthHandler(keys["CONSUMER_KEY"], keys["CONSUMER_SECRET"])
    auth.secure = True
    auth.set_access_token(keys["ACCESS_TOKEN"], keys["ACCESS_SECRET"])
    return tw.API(auth)


def readMetadata(inputfile):
	line = inputfile.readline()
	data = line.split('\t')
	data = map(lambda x: x.replace('\n',''), data)
	if(len(data) == 2):
		return data[1]
	elif(len(data) < 2):
		return None


def retrieveTweets(outputfile_path):
	index = 0
	api = returnAPI(index)
	lastID = ""
	nRequests = 0

	with open(outputfile_path, 'w') as outputfile:

		for status in tw.Cursor(api.user_timeline, id = TW_ACCOUNT).items(3000):
			jsonElement = json.dumps(status._json)
			lastID = status._json["id_str"]
			outputfile.write(jsonElement + '\n')
			nRequests += 1

			if(nRequests % 200 == 0):
				print("Account: %s, requests: %d, key: %index" % (TW_ACCOUNT, nRequests, index))
				index += 1
				api = returnAPI(index)

	return lastID


def main():
	setup()
	filename = TW_ACCOUNT + ".txt"

	inputfile_path = os.path.join(RAW_DATA_DIR, filename)
	global LAST_ID, inputfile

	with open(inputfile_path, 'r') as inputfile:
		LAST_ID = readMetadata(inputfile)

		if(LAST_ID == None):
			LAST_ID = retrieveTweets(inputfile_path)
			print LAST_ID


if __name__ == '__main__':
	main()