__author__ = 'ommirandap'

import os
import csv

import pandas as pd

import DataProcessing


def name_input_files(input_path):
    print("Listing data files from: " + input_path)
    opj = os.path.join
    files = [opj(input_path, filename) for filename in os.listdir(input_path)
             if os.path.isfile(opj(input_path, filename)) and
             os.access(opj(input_path, filename), os.R_OK)
             and filename.endswith(".tsv")]
    return files


def set_up_DataFrame(input_files):
    table_collection = []
    input_files.sort()
    columns = ["Timestamp", "userID", "userName", "tweetID", "text"]
    print("Constructing the DataFrames")
    
    for single_file in input_files:
        try:
            single_table = pd.read_table(single_file, index_col = "tweetID",
                                         header = None, names = columns,
                                         quoting = csv.QUOTE_NONE)
            table_collection.append(single_table)
        except pd.parser.CParserError as detail:
            print single_file, detail
    print("Merging in one DataFrame")
    complete_table = pd.concat(table_collection)
    print("DataFrame ready!")
    return complete_table


def get_tweets_from_username(dataframe_input, username):
    query_text = "userName in (\"" + username + "\")"
    
    tweets_collection = dataframe_input.query(query_text)
    tweet_list = []
    for tweet in tweets_collection['text']:
        tweet_list.append(tweet)
    
    return tweet_list


def main():
    input_path = "/home/ommirandap/PRISMA/dynews/data-headlines/tsv-copy"
    # input_path = sys.argv[0]
    df = set_up_DataFrame(name_input_files(input_path))
    
    for i in get_tweets_from_username(df, "elmostrador"):
        print i
        print DataProcessing.remove_stopwords(i)


if __name__ == '__main__':
    main()
