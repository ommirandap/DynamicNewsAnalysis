from operator import itemgetter
import numpy
from theano.compile.function_module import orig_function

__author__ = 'ommirandap'


# Asumo que recibo como input una lista
# [[str1_t1, str2_t1, str3_t1, ...], [str1_t2, str1_t2, ...], ...]
# Lista de set de palabras

MAX_TOPICS_PER_HOUR = 6
KEYWORDS_PER_TOPIC = 2
MATCH_NO = 3


def collect_keywords(groups_of_keywords, new_keywords):
    check_flag = 0

    if (len(groups_of_keywords) == 0):
        a = {}
        for each in new_keywords:
            a[each] = 1
        groups_of_keywords.append(a)
        return groups_of_keywords

    intersection_length = []
    for group in groups_of_keywords:
        orig_keywords = set(group.keys())
        common_keywords = orig_keywords.intersection(new_keywords)
        intersection_length.append(len(common_keywords))

    max_score_ind = intersection_length.index(max(intersection_length))

    if (intersection_length[max_score_ind] >= MATCH_NO):
        check_flag = 1
        for each in new_keywords:
            if each in groups_of_keywords[max_score_ind].keys():
                groups_of_keywords[max_score_ind][each] = \
                    groups_of_keywords[max_score_ind][each] + 1
            else:
                groups_of_keywords[max_score_ind][each] = 1

    if (check_flag == 0):
        a = {}
        for each in new_keywords:
            a[each] = 1
        groups_of_keywords.append(a)

    return groups_of_keywords


def getKeywords_fromHeadlines(list_of_tweets):
    # INPUT: lista de set de words
    groups_of_keywords = []
    # To list of list of words
    headlines = []

    for t in list_of_tweets:
        a = []
        for w in t:
            a.append(w)
        headlines.append(a)

    for i in range(len(headlines)):
        for j in range(len(headlines))[i + 1:]:
            if (i == j):
                continue
            struct = jaccard_similarity(headlines[i], headlines[j])
            if (struct['no_common_words'] < MATCH_NO):
                continue
            groups_of_keywords = collect_keywords(groups_of_keywords,
                                                  struct['common_words'])

    scores = []
    i = 0
    for group in groups_of_keywords:
        avg = 0
        for each_key in group.keys():
            avg = avg + group[each_key]
        scores.append(float(avg) / len(group.keys()))
        i = i + 1

    sorted_indices = numpy.argsort(scores)
    sorted_indices = sorted_indices[::-1]

    # for i in range(len(sorted_indices)):
    #    index = sorted_indices[i]
    #    print scores[index]
    #    for each_key in groups_of_keywords[index].keys():
    #        print each_key + ' ' + str(groups_of_keywords[index][each_key])

    return groups_of_keywords


def compare(e1, e2):
    '''
    e1 = {kw1: sc1, kw2: sc2}
    e2 = {kw3: sc3, kw4: sc4}
    '''
    score1 = sum(e1.values()) / len(e1.values())
    score2 = sum(e2.values()) / len(e2.values())

    return score2 - score1


def get_keywords(list_of_tweets):
    # INPUT: lista de sets de words
    groups = getKeywords_fromHeadlines(list_of_tweets)
    groups = sorted(groups, cmp = compare)

    if len(groups) > MAX_TOPICS_PER_HOUR:
        groups = groups[0:MAX_TOPICS_PER_HOUR]

    ret = []

    for g in groups:
        most_relevant_kws = sorted(g.iteritems(), key = itemgetter(1),
                                   reverse = True)
        ret.append(tuple(most_relevant_kws[0:KEYWORDS_PER_TOPIC]))

    return ret


def get_tweets_keywords(tweets):
    day_tweets = []
    day_keywords = []

    # For filename... eso significa que es por hora (?)
    day_keywords.append(get_keywords(t for t in tweets if len(t) > 0))
    day_tweets.extend(tweets)

    return (day_tweets, day_keywords)


def jaccard_similarity(sentence1, sentence2):
    # Calculo del indice de Jaccard. Inter versus Union
    # Esto no deberia tocarlo mas
    # words1 = set(sentence1.split(' '))
    # words2 = set(sentence2.split(' '))

    words1 = set(sentence1)
    words2 = set(sentence2)
    common = words1.intersection(words2)
    total = words1.union(words2)

    similarity_struct = {}
    similarity_struct['sim'] = len(common) / float(len(total))
    similarity_struct['no_common_words'] = len(common)
    similarity_struct['common_words'] = common

    return similarity_struct


def main():
    pass


if __name__ == '__main__':
    main()
