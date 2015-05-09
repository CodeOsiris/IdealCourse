#!/usr/bin/python
import json
import pickle
from math import log, sqrt
from operator import itemgetter
from nltk.stem import SnowballStemmer
from nltk.corpus import wordnet
import pprint

print 'Loading course info'
info = json.load(open('extend.json'))
print 'Loading stop words'
stopwords = pickle.load(open('stopwords.pickle'))
print 'Loading weight table'
idftable = pickle.load(open('idftable.pickle'))
idftable_desc = pickle.load(open('idftable_desc.pickle'))
docs = len(info)
stemmer = SnowballStemmer('english')

def mean(lst):
    if len(lst) == 0:
        return 0
    return sum(lst) * 1.0 / len(lst)

def stddev(lst):
    if len(lst) == 0:
        return 0
    variance = 0
    m = mean(lst) * 1.0
    for elem in lst:
        variance += (elem - m) ** 2
    variance /= len(lst)
    return sqrt(variance)

def totalhits(query):
    keywords = ''
    for word in query:
        if word in stopwords:
            continue
        keywords += word + ' '
    params = {
            'action':'query',
            'list':'search',
            'format':'json',
            'srsearch':keywords,
            'srwhat':'text',
            'srinfo':'totalhits',
            }
    request = api.APIRequest(site, params)
    result = request.query(querycontinue=False)
    totalhits = int(result['query']['searchinfo']['totalhits'])
    return totalhits

def query_to_institute(query, course):
    if len(query) == 0:
        return 0
    score = 0
    match = set()
    for word in query:
        if word in course['school_bag']:
            score += 0.5
            match.add(word)
        if word in course['department_bag']:
            score += 1
            match.add(word)
    return score * pow((len(match) + 1) * 1.0 / (len(query) + 1), 0.95)

def query_to_title(query, course):
    if len(query) == 0:
        return 0
    score = 0
    match = set()
    for word in query:
        if word in course['title_bag']:
            score += 1
            match.add(word)
    return score * pow((len(match) + 1) * 1.0 / (len(query) + 1), 0.95)

def query_to_description(query, course):
    if len(query) == 0:
        return 0
    score = 0
    norm = 0
    match = {}
    for word in course['description_bag']:
        if word in query:
            score += course['description_bag'][word] * log(docs * 1.0 / (idftable_desc[word] + 1))
            if word not in match:
                match[word] = 0
            match[word] += 1
        norm += course['description_bag'][word] ** 2
    score /= sqrt(norm + 1) * sqrt(len(query) + 1)
    val = match.values()
    m = mean(val)
    std = stddev(val)
    return score * pow((len(match) + 1) * 1.0 / (len(query) + 1), 0.95) * m / (std + 1)

def query_to_supplement(query, course):
    if len(query) == 0:
        return 0
    score = 0
    norm = 0
    match = {}
    for word in course['supplement_bag']:
        if word in query:
            score += course['supplement_bag'][word] * log(docs * 1.0 / (idftable[word] + 1))
            if word not in match:
                match[word] = 0
            match[word] += 1
        norm += course['supplement_bag'][word] ** 2
    score /= sqrt(norm + 1) * sqrt(len(query) + 1)
    val = match.values()
    m = mean(val)
    std = stddev(val)
    return score * pow((len(match) + 1) * 1.0 / (len(query) + 1), 0.95) * m / (std + 1)

def score(query, course, coeff, norm):
    if len(course['description_bag']) > 0:
        q2i = query_to_institute(query, course)
        q2t = query_to_title(query, course)
        q2d = query_to_description(query, course)
        q2s = query_to_supplement(query, course)
        norm['q2i'] += q2i
        norm['q2t'] += q2t
        norm['q2d'] += q2d
        norm['q2s'] += q2s
        return (q2i, q2t, q2d, q2s)
    else:
        q2i = query_to_institute(query, course)
        q2t = query_to_title(query, course)
        q2s = query_to_supplement(query, course)
        norm['q2i'] += q2i
        norm['q2t'] += q2t
        norm['q2d'] += q2s
        return (q2i, q2t, q2s, 0)

def weighted_score(scores, norm):
	return coeff['q2i'] * scores[0] / norm['q2i'] + coeff['q2t'] * scores[1] / norm['q2t'] + coeff['q2d'] * scores[2] / norm['q2d'] + coeff['q2s'] * scores[3] / norm['q2s']

def generate_synset(query):
    unique = set()
    unique_syn = set()
    for word in query:
        word = word.lower()
        if word in stopwords:
            continue
        unique.add(stemmer.stem(word))
        synset = wordnet.synsets(word)
        for syn in synset:
            if syn.pos == synset[0].pos:
                lemmas = syn.lemma_names()
                for lemma in lemmas:
                    lemma = lemma.split('_')
                    for seg in lemma:
                        if seg in stopwords:
                            continue
                        unique_syn.add(stemmer.stem(seg))
    return list(unique), list(unique_syn)

coeff = {
        'q2i' : 0.2,
        'q2t' : 0.75,
        'q2d' : 1.2,
        'q2s' : 0.35,
        }

sorted_list = []
for course in info:
    sorted_list.append((course['title'], course['department'], course['school'], 0, 0, 0, 0))

while True:
    norm = {
            'q2i' : 0,
            'q2t' : 0,
            'q2d' : 0,
            'q2s' : 0,
            }

    input_q = raw_input('Query: ').split()

    if len(input_q) == 0:
        break
    else:
        query, synsets = generate_synset(input_q)
        print 'Stemmed query words: ', ' '.join(query)
        syn_coeff = 0.2
        for i in range(len(sorted_list)):
            score_exact = score(query, info[i], coeff, norm)
            score_synset = score(synsets, info[i], coeff, norm)
            for norm_category in norm:
                if norm[norm_category] == 0:
                    norm[norm_category] = 1
            sorted_list[i] = (sorted_list[i][0], sorted_list[i][1], sorted_list[i][2], score_exact[0] + syn_coeff * score_synset[0], score_exact[1] + syn_coeff * score_synset[1], score_exact[2] + syn_coeff * score_synset[2], score_exact[3] + syn_coeff * score_synset[3])
        top_list = sorted(sorted_list, key = lambda item : weighted_score(itemgetter(-4, -3, -2, -1)(item), norm), reverse = True)[ : 20]
        for i in range(len(top_list)):
            course = top_list[i]
            pprint.pprint({'Title':course[0], 'Department':course[1], 'School':course[2]})
