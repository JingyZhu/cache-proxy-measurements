from sklearn import tree
from sklearn.model_selection import StratifiedKFold
from sklearn import metrics
from sklearn.model_selection import train_test_split
from urllib.parse import urlparse
import numpy as np
import pickle
import json
import os
from common import *


X, y = get_dataset()
print('====== Readin Finished ======')
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, stratify=y, random_state=3)
clf = tree.DecisionTreeClassifier(class_weight={-1: 2.5, 1:1})
clf.fit(X_train, y_train)
print('====== Trainned Finished ======')

metrics_list = ['accuracy', 'f1-score', 'auroc', 'precision', 'sensitivity', 'specificity']

for m in metrics_list:
    print(m, ': ', performance(clf, X_train, y_train, metric=m))
print('\n\n')
for m in metrics_list:
    print(m, ': ', performance(clf, X_test, y_test, metric=m))
print('\n\n')

print(metrics.confusion_matrix(y_test, clf.predict(X_test)))
# save_to_pickle('latest.pickle', clf)