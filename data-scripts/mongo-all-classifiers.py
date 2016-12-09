#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pymongo import MongoClient
from matplotlib.colors import ListedColormap
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_moons, make_circles, make_classification
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC, LinearSVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis

client = MongoClient()
db = client.github
collection = db.languages
data = pd.DataFrame(list(collection.find()))
data.drop("_id", axis=1, inplace=True)
data = data.drop_duplicates()
data = data.fillna(0)
data[data > 0] = 1
label_name = "Python"
y = data[label_name]
X = data.drop(label_name, axis=1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

names = ["Nearest Neighbors", "Linear SVM", "RBF SVM", "Gaussian Process",
         "Decision Tree", "Random Forest", "Neural Net", "AdaBoost",
         "Naive Bayes", "QDA"]

classifiers = [
    KNeighborsClassifier(),
    LinearSVC(),
    SVC(),
    GaussianProcessClassifier(1.0 * RBF(1.0), warm_start=True,
        copy_X_train=False),
    DecisionTreeClassifier(),
    RandomForestClassifier(),
    MLPClassifier(),
    AdaBoostClassifier(),
    GaussianNB(),
    QuadraticDiscriminantAnalysis()]

# classifiers = [
#     KNeighborsClassifier(3),
#     SVC(kernel="linear", C=0.025),
#     SVC(gamma=2, C=1),
#     GaussianProcessClassifier(1.0 * RBF(1.0), warm_start=True),
#     DecisionTreeClassifier(max_depth=5),
#     RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
#     MLPClassifier(alpha=1),
#     AdaBoostClassifier(),
#     GaussianNB(),
#     QuadraticDiscriminantAnalysis()]

KN = {
        "n_neighbors": [1, 2, 3, 4, 5],
        "weights": ["uniform", "distance"],
        "algorithm": ["auto", "ball_tree", "kd_tree", "brute"],
        }

SVC_linear = {
        "C": [0.01, 0.1, 1.0],
        }

SVC = {
        "C": [0.01, 0.1, 1.0],
        "gamma": [1.0, 2.0, 3.0],
        }

GP = {
        }

DT = {
        "criterion": ["gini", "entropy"],
        "splitter": ["best", "random"],
        "max_features": ["auto", "sqrt", "log2"],
        "max_depth": [None, 1, 3, 5],
        }

RT = {
        "n_estimators": [10, 20, 30],
        "criterion": ["gini", "entropy"],
        "max_features": ["auto", "sqrt", "log2"],
        "max_depth": [None, 1, 3, 5],
        }

MLP = {
        "hidden_layer_sizes": [(50,), (100,), (300,)],
        "activation": ["identity", "logistic", "tanh", "relu"],
        "solver": ["lbfgs", "sgd", "adam"],
        "alpha": [0.0001, 0.001, 0.01, 0.1, 1],
        "learning_rate": ["constant", "invscaling", "adaptive"],
        }

Ada = {
        "n_estimators": [10, 25, 50],
        "learning_rate": [0.01, 0.1, 1],
        "algorithm": ["SAMME", "SAMME.R"],
        }

GNB = {}

QDA = {}

params_lists = [KN, SVC_linear, SVC, GP, DT, RT, MLP, Ada, GNB, QDA]

parameters = dict(list(zip(names, params_lists)))

# # iterate over classifiers
# for name, clf in zip(names, classifiers):
#     clf.fit(X_train, y_train)
#     score = clf.score(X_test, y_test)
#     print("{} has score: {}".format(name, score))

# GridSearchCV over all classifiers
for name, clf in zip(names, classifiers):
    classifier = GridSearchCV(clf, parameters[name])
    classifier.fit(X_train, y_train)
    score = classifier.score(X_test, y_test)
    print("Best estimator for {}: {}".format(name, classifier.best_estimator_))
    print("{} has score: {}".format(name, score))
