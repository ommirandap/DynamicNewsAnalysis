import sys

from DataManage import DataExtractor

__author__ = 'ommirandap'

n_args = len(sys.argv)

if n_args == 2:
	arg1 = sys.argv[1]
	arg2 = None
elif n_args == 3:
	arg1 = sys.argv[1]
	arg2 = sys.argv[2]
else:
	exit()

# Testing files
# Extractor.process_tweet_json_file(arg1, arg2)

# Testing folders
DataExtractor.process_tweet_folder(arg1, arg2)

# Testing pandas
#t = Extractor.tsv_tweets_pandas_dataframe(arg1)
#print(t)

#print Utilities.remove_stopwords(arg1)
