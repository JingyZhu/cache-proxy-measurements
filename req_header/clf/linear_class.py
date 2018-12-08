from sklearn.svm import SVC, LinearSVC
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import train_test_split
import numpy as np
import os
from common import *

# [cdn/asset, Font, cache_ext, isGET, XHR, Document, Uncache_ext, content-type/content-length, coockies]
X = []
y = []
kernel = 'linear'


X, y = get_dataset()
print('====== Readin Finished ======')
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, stratify=y, random_state=3)
clf = SVC(kernel=kernel, C=100, class_weight={-1: 2.75, 1: 1})
clf.fit(X_train, y_train)
print('====== Trainned Finished ======')

metrics_list = ['accuracy', 'f1-score', 'auroc', 'precision', 'sensitivity', 'specificity']
for m in metrics_list:
    print(m, ': ', performance(clf, X_test, y_test, metric=m))

print('\n\n')
if kernel == 'linear':
    print(list(zip(feature_lists, clf.coef_[0].tolist())))
    print('\n\n')

print(metrics.confusion_matrix(y_test, clf.predict(X_test)))
# save_to_pickle('latest.pickle', clf)