__author__ = 'ommirandap'

import pandas as pd


def tweets_by_dates(df, column_name, start_date, end_date):
    if start_date > end_date:
        print "Start day cannot happen before the end. Please don't break the time"
        return None
    mask = (df[column_name] > start_date) & (df[column_name] <= end_date)
    return df.loc[mask]


def tweet_array_per_hour_by_day(df, column_name, day):
    '''
    Given the Dataframe of tweets (normalized -> df['t'] = df['t'].map(clean))
    :param df:
    :param column_name:
    :param day:
    :return: [(Timestamp1, [{str1, str2, str3, ...}, ...]), ...]
                <=>
            Array(Tuple(Timestamp, Array(Set(String))))
    '''
    tweet_array = []
    hours = pd.date_range(day, periods = 24, freq = 'H')

    for h in hours:
        mask = (df[column_name] > h) & (df[column_name] < h + 1)
        res = df.loc[mask]
        tweets_list = []
        for t in res['text'].tolist():
            tweets_list.append(set(t.split()))
        tweet_array.append((h, tweets_list))

    return tweet_array
