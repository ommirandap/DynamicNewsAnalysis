__author__ = 'ommirandap'

import os
import csv
import pandas as pd


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



def main():
    pass


def load_df_all_days(
        input_path = "/home/ommirandap/PRISMA/dynews/data-headlines"
                     "/tsv-copy"):
    '''
    :param input_path: input folder where the tsv files are
    :return: a Pandas Dataframe containing all tweet data, indexed by tweetID
    with all Timestamps parsed as pandas dates.
    '''

    # Name the files
    opj = os.path.join
    files = [opj(input_path, filename) for filename in os.listdir(input_path)
             if os.path.isfile(opj(input_path, filename)) and
             os.access(opj(input_path, filename), os.R_OK)
             and filename.endswith(".tsv")]

    # Reading the data an merging it on a DataFrame
    hourly_dataframe = []
    columns = ["Timestamp", "userID", "userName", "tweetID", "text"]

    print "This might take a while. Sorry, but there are A LOT of tweets"

    for doc in files:

        try:
            single_table = pd.read_table(doc, parse_dates = ['Timestamp'],
                                         index_col = ['tweetID'], header = None,
                                         names = columns,
                                         quoting = csv.QUOTE_NONE)
            hourly_dataframe.append(single_table)
        except (pd.parser.CParserError) as detail:
            print doc, detail

    concatenated_tables = pd.concat(hourly_dataframe)

    return concatenated_tables


if __name__ == '__main__':
    main()
