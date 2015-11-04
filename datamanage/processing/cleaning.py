__author__ = 'ommirandap'

from unidecode import unidecode
from nltk.corpus import stopwords
import string
import re


'''
Regular expressions obtained from Jorge's data cleaning
'''
remove = re.compile(r"\b\S{1,2}\b|#\S+|@\w+|\bhttps?\S+\b")
replace = re.compile(r"\s+|[!\"#$%&\'()*+,-./:;<=>?@\[\\\]^_`{|}~]")
shorten = re.compile(r"\s+")
normalize_text = lambda text: \
    shorten.sub(" ", (replace.sub(" ", remove.sub("", text.lower())))).strip()

SPANISH_STOPWORDS = set(stopwords.words('spanish'))
SPANISH_STOPWORDS_NORM = set(map(normalize_text, stopwords.words('spanish')))
FINAL_SW = SPANISH_STOPWORDS.union(SPANISH_STOPWORDS_NORM)
#SPANISH_STOPWORDS_NORM = map
ls# ((
#    lambda text: unidecode(text).strip().lower().replace('\n', ' ').
#    replace('\r', '')), SPANISH_STOPWORDS)

def clean_text(text):

    pre_text = normalize_text(text).split()
    post_text = filter(remove_stopword_lambda(FINAL_SW), pre_text)

    return ' '.join(post_text)


def remove_stopword_lambda(bag):
    return lambda word: word not in bag


def remove_url_filter(word):
    return not is_url(word)


def remove_only_digits(word):
    return not word.isdigit()


def remove_mentions(word):
    return not is_mention(word)


def is_url(text):
    if re.match('^https?:\/\/.*', text) or re.match('^http:\/\/.*', text):
        return True
    return False


def is_mention(text):
    if re.match('(?:\@)\S+', text):
        return True
    return False


def remove_punctuation(entire_tweet):
    text_wo_punctuation = entire_tweet.translate(string.maketrans("", ""),
                                                 string.punctuation)
    return text_wo_punctuation


def remove_stopwords(text, stopwords = []):
    text_list = text.split()
    stopwords_set = set(stopwords)
    internal_stopwords = SPANISH_STOPWORDS.union(stopwords_set)
    text_wo_url = filter(remove_url_filter, text_list)
    text_wo_mentions = filter(remove_mentions, text_wo_url)
    text_wo_digits = filter(remove_only_digits, text_wo_mentions)
    text_wo_stopwords = filter(remove_stopword_lambda(internal_stopwords),
                               text_wo_digits)
    text_wo_stopwords_joined = ' '.join(text_wo_stopwords)
    text_wo_punctuation = remove_punctuation(text_wo_stopwords_joined)
    return text_wo_punctuation

