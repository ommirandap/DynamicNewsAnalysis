import codecs
import json
import unidecode
import os

__author__ = 'ommirandap'

"""
This module it's gonna be the main script to process the raw data (many json
files that contains an array of N tweets API-styled) that resides in the
[folder] parameter
"""


def process_tweet_json_file(filename_input, filename_output=None):
    """This function will open a twitter-json file (stored at filename_input)
    and process every tweet extracting the important fields (timestamp, userID,
    tweetID and text) and writing those on a tsv file (created and stored at
    filename_output)

    :type filename_input: str
    :type filename_output: str

    Args:
            filename_input (str): The complete path of the input file
            filename_output (str): The complete path of the output file. If it
            is not provided, the output filename will be the same as the input
            with the tsv extension.

    """

    if filename_output is None:
        filename_output = filename_input.replace('.json', '.tsv')

    with codecs.open(filename_input, 'r', 'utf-8') as f_i:
        with codecs.open(filename_output, 'wb', 'utf-8') as f_o:
            parsed_json = json.loads(f_i.read())
            for tweet in parsed_json:
                outline_list = [tweet['created_at'],
                                tweet['user']['id_str'],
                                tweet['user']['screen_name'],
                                tweet['id_str'],
                                normalize_text(tweet['text'])]
                outline = '\t'.join(outline_list) + '\n'
                # outline = outline.encode("utf-8")
                f_o.write(outline)


def normalize_text(tweet):
    """This function will normalize the tweet (text) deleting unnecessary
    spaces, converting the letters to lowercase and deleting the carriage
    returns. Also, read all the characters safely with unidecode.

    :type tweet: str

    Args:
            tweet (str): The text to be normalized.

    """

    normalized_tweet = unidecode.unidecode(tweet).strip().lower()
    return normalized_tweet.replace('\n', ' ').replace('\r', '')


def process_tweet_folder(input_path, output_path=None):
    """This function will process a directory that contains twitter-json files
    converting all of the to tsv files, extracting the important fields (See:
    process_tweet_json_file)

    :type input_path: str
    :type output_path: str

    Args:
            input_path (str): The absolute path of the folder containing the
            json files
            output_path (str): The absolute path of the folder the tsv files
            will be written. If not specified, the output files will be written
            at the same folder that the input.

    """

    # Path joiner generator
    opj = os.path.join
    # Files to be read
    files = [filename for filename in os.listdir(input_path)
             if os.path.isfile(opj(input_path, filename)) and
             os.access(opj(input_path, filename), os.R_OK) and
             filename.endswith(".json")]

    for input_file in files:
        input_complete_path = opj(input_path, input_file)
        if output_path is None:
            process_tweet_json_file(input_complete_path)
        else:
            output_complete_path = opj(output_path,
                                       input_file.replace(".json", ".tsv"))
            process_tweet_json_file(input_complete_path,
                                    output_complete_path)
