__author__ = 'ommirandap'

from itertools import chain
import igraph as ig


def get_max_tf_idf(hourly_topics, all_keywords):
    pass


def get_tf_idf(tweets, topic_keywords, names):
    hourly_topics = map(lambda h:
                        map(lambda t:
                            tuple(map(lambda kw: kw[0], t)),
                            h),
                        topic_keywords)

    day_topics = map(lambda t:
                     tuple(map(lambda keyword: keyword[0], t)),
                     chain.from_iterable(topic_keywords))

    all_keywords = set().union(*(set(d) for d in day_topics))

    max_tf_idf = get_max_tf_idf(hourly_topics, all_keywords)
    g = ig.Graph(n = len(all_keywords), directed = False)
    g.vs["name"] = list(all_keywords)

    return
