import datetime
import gzip
import sys

from apps import headlines_collector
from MauriciosAlgorithms import twitter_scripts as ts
import words
from twitter_db import *
import simplejson as json
import data_collector_tweets

err = lambda m: sys.stderr.write(datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S') + ' - ' + str(m) + '\n')


def compare(e1, e2):
    """
    e1 = {kw1: sc1, kw2: sc2}
    e2 = {kw3: sc3, kw4: sc4}
    """
    score1 = sum(e1.values()) / len(e1.values())
    score2 = sum(e2.values()) / len(e2.values())
    return score2 - score1

format_date = lambda d: datetime.datetime.strftime(d, '%Y-%m-%d_%H%M%S')

headlines_dir = '/home/mquezada/data/news2/headlines_data'
temp_dir = '/home/mquezada/data/news2/tmp'
news_accounts_file = '/home/mquezada/code/twitter/news_accounts.txt'
NUM_EVENTS = 6

with open(news_accounts_file) as f:
    news_accounts = f.read().split(',')

headlines_tweets = []
headlines = []
now = datetime.datetime.utcnow()
one_hour_before = now - datetime.timedelta(hours=1)


err("Getting headlines from %s until %s" % (str(one_hour_before), str(now)))
for user in news_accounts:
    # getting headlines from 1 user
    timeline = headlines_collector.user_timeline(user, from_date=one_hour_before, use_bearer_token=True, json_dump=False)

    if timeline is None:
        continue

    for tweet in timeline:
        # process tweet
        actual_tweet = tweet.get('retweeted_status', tweet)
        text = unicode(actual_tweet['text'])
        text = ' '.join(words.clean_and_tokenize(text, remove_mentions=True, remove_hashtags=True))

        headlines.append(text)
        headlines_tweets.append(tweet)

err("Total: %d headlines" % len(headlines))

# extracting keywords from headlines
groups = ts.getKeywords_fromHeadlines(headlines, "/dev/null")
groups = sorted(groups, cmp=compare)

selected = []
for g in groups:
    tent =  sorted(g.iteritems(), key=lambda t: t[1], reverse=True)
    for word_list in tent:
        #if word_list[0] not in selected:
        selected.append(word_list[0])
        if len(selected) % 2 == 0:
            break
    if len(selected) == NUM_EVENTS * 2:
        break
top_keywords = []

while len(selected) > 0:
    top_keywords.append((selected.pop(), selected.pop()))
err("Keywords extracted: %s" % str(top_keywords))


# headlines
with open(headlines_dir + '/' + format_date(now) + '_headlines.txt', 'w') as f:
    for headline in headlines:
        print >>f, headline
err("Wrote %s" % (headlines_dir + '/' + format_date(now) + '_headlines.txt'))

# keyword groups
with open(headlines_dir + '/' + format_date(now) + '_keywords_scores.dict', 'w') as f:
    print >>f, groups
err("Wrote %s" % (headlines_dir + '/' + format_date(now) + '_keywords_scores.dict'))

# headlines tweets
f = gzip.open(headlines_dir + '/' + format_date(now) + '_headlines_tweets.json.gz', 'w')
f.write(json.dumps(headlines_tweets))
f.close()
err("Wrote %s" % (headlines_dir + '/' + format_date(now) + '_headlines_tweets.json.gz'))

# keyword pair tweets
err("Starting tweets collection")
data_collector_tweets.collect_tweets(top_keywords, now, temp_dir)
err("Ended search\n")
