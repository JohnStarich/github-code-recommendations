#!/usr/bin/env python3

import re
import numpy as np
import pandas as pd
from pymongo import MongoClient
from collections import Counter
import math
from sklearn.metrics import accuracy_score

client = MongoClient()
db = client.github
collection = db.events
data = list(collection.find(
    {"type": "PullRequestEvent", "payload.pull_request.merged": True, "payload.pull_request.head.repo.language": "Python", "word_diff": {"$exists": True, "$ne": ""}},
    {"word_diff": 1},
))

print("Data size = {}".format(len(data)))

plus = re.compile("{\+ (.*?) \+}", flags=re.VERBOSE | re.DOTALL)
minus = re.compile("\[- (.*?) -\]", flags=re.VERBOSE | re.DOTALL)

adds = Counter()
removes = Counter()

def get_matches(data):
    add = plus.findall(data)
    remove = minus.findall(data)
    for match in add:
        match = cleanup(match)
        if match:
            for line in match.split():
                if line:
                    adds[line] += 1
    for match in remove:
        match = cleanup(match)
        if match:
            for line in match.split():
                if line:
                    removes[line] += 1
    return add, remove

def cleanup(match):
    return match.replace(" ", "").replace("\t", "")

for datum in data:
    get_matches(datum["word_diff"])

ngram_add = {}
ngram_remove = {}

def getNGrams(text, n):
    text = (" " * (n - 1)) + text + " "
    return [text[i:i+n] for i in range(len(text) - n + 1)] 

def getConditionalCounts(sentences, n):
    condCounts = {}
    for sentence in sentences:
        ngrams = getNGrams(sentence, n)
        for gram in ngrams:
            context, lastChar = gram[:n - 1], gram[-1]
            condCounts.setdefault(context, {}).setdefault(lastChar, 0)
            condCounts[context][lastChar] += 1
    return condCounts

class CharNGram:
    def __init__(self, language, conditionalCounts, n):
        self.language = language
        self.condCounts = conditionalCounts
        self.n = n
        self._getNormalizedCounts()

    def _contextcounttotals(self, ctx):
        if ctx in self.condCounts:
            return sum(self.condCounts[ctx].values())
        else:
            return 0

    def _getNormalizedCounts(self):
        for ctx, counts in self.condCounts.items():
            for lastChar, count in counts.items():
                self.condCounts[ctx][lastChar] = \
                    (count + 1)/float(26 + self._contextcounttotals(ctx))

        """
        Using conditional frequency distribution,
        calculate and return p(c | ctx)
        """
    def ngramProb(self, ctx, c):
        return self.condCounts.get(ctx, {}).get(c, 1.0/float(26 + self._contextcounttotals(ctx)))

        """ Multiply ngram probabilites for each ngram in word """
    def wordProb(self, word):
        prob = 1.0
        for ctx, counts in getConditionalCounts([word], self.n).items():
            for lastChar, count in counts.items():
                prob *= self.ngramProb(ctx, lastChar) * count
        return math.log(prob)

class CodeModel:
    def __init__(self, models):
        self.models = models

    def guess(self, word):
        highestProb = max(model.wordProb(word.lower())
            for model in self.models)
        guess = [model for model in self.models
                 if model.wordProb(word.lower()) == highestProb]
        return guess[0].language

    def prob(self, language, word):
        return [model for model in self.models
                if model.language == language][0].wordProb(word.lower())

ngram_adds = getConditionalCounts(adds.keys(), 5)
ngram_removes = getConditionalCounts(removes.keys(), 5)

good = CharNGram("Good", ngram_adds, 5)
bad = CharNGram("Bad", ngram_removes, 5)

cm = CodeModel([good, bad])

correct = 0
incorrect = 0
pred_good = []
pred_bad = []

for match in adds:
    try:
        guess = cm.guess(match)
    except:
        continue
    if guess == "Good":
        correct += 1
        pred_good.append("Good")
    else:
        incorrect += 1
        pred_good.append("Bad")

def good():
    for _ in pred_good:
        yield "Good"

print("Accuracy for Good Code: {}".format(accuracy_score(list(good()), pred_good)))

for match in removes:
    try:
        guess = cm.guess(match)
    except:
        continue
    if guess == "Bad":
        correct += 1
        pred_bad.append("Bad")
    else:
        incorrect += 1
        pred_bad.append("Good")

def bad():
    for _ in pred_bad:
        yield "Bad"

print("Accuracy for Bad Code: {}".format(accuracy_score(list(bad()), pred_bad)))
print("Ratio: Correct/Total = {}".format(correct/(correct + incorrect)))
print(incorrect + correct)

