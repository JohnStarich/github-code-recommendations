#!/usr/bin/env python3

import numpy as np
import pandas as pd
from pymongo import MongoClient
from sklearn.kernel_approximation import RBFSampler
from sklearn.model_selection import (train_test_split,GridSearchCV)
from sklearn.metrics import (accuracy_score,roc_auc_score)

from sklearn.linear_model import SGDClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
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

sgd = SGDClassifier()
sgd.fit(X_train, y_train)
y_pred = sgd.predict(X_test)
print("SGD Accuracy: {}".format(accuracy_score(y_test, y_pred)))

rbf_feature = RBFSampler(gamma=1, random_state=1)
X_features = rbf_feature.fit_transform(X)
sgd_kernel = SGDClassifier()
sgd_kernel.fit(X_features, y)
print("SGD Score with kernel approximation: {}".format(sgd_kernel.score(X_features, y)))

# print("**** WITH GridSearchCV ****")
# parameters = {
# 	'loss': ['hinge', 'modified_huber', 'squared_hinge'],
# 	'penalty': ['none', 'l2', 'l1', 'elasticnet'],
# 	'n_iter': [1, 2, 3, 4, 5],
# 	'alpha': [0.0001, 0.001, 0.01, 0.1],
# 	'learning_rate': ['constant', 'optimal', 'invscaling'],
# 	'eta0': [1.0],
# }
# sgd3 = SGDClassifier()
# clf = GridSearchCV(sgd3, parameters)
# clf.fit(X_train, y_train)
# print(clf.best_estimator_)
# y_pred2 = clf.predict(X_test)
# print("Accuracy with GridSearchCV: {}".format(accuracy_score(y_test, y_pred2)))

mlp = MLPClassifier()
mlp.fit(X_train, y_train)
y_pred1 = mlp.predict(X_test)
print("MLP Accuracy: {}".format(accuracy_score(y_test, y_pred1)))

knc = KNeighborsClassifier()
knc.fit(X_train, y_train)
y_pred2 = knc.predict(X_test)
print("KNC Accuracy: {}".format(accuracy_score(y_test, y_pred2)))

svc = SVC()
svc.fit(X_train, y_train)
y_pred3 = svc.predict(X_test)
print("SVC Accuracy: {}".format(accuracy_score(y_test, y_pred3)))

dtc = DecisionTreeClassifier()
dtc.fit(X_train, y_train)
y_pred4 = dtc.predict(X_test)
print("DTC Accuracy: {}".format(accuracy_score(y_test, y_pred4)))

nb = GaussianNB()
nb.fit(X_train, y_train)
y_pred5 = nb.predict(X_test)
print("NB Accuracy: {}".format(accuracy_score(y_test, y_pred5)))
