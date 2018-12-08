from sklearn.svm import SVC, LinearSVC
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import train_test_split
from sklearn.externals.joblib import Parallel, delayed
from tqdm import tqdm

import numpy as np
import os
from common import *

# [cdn/asset, Font, cache_ext, isGET, XHR, Document, Uncache_ext, content-type/content-length, coockies]
X = []
y = []
kernel = 'rbf'

X, y, weights, median = get_weighted_dataset()
print('====== Readin Finished ======')
X_train, X_test, y_train, y_test, weight_train, weight_test = train_test_split(X, y, weights, test_size=0.20, stratify=y, random_state=3)


def fit(class_weight={-1:1, 1:1}):
    clf = SVC(kernel=kernel, C=1, class_weight=class_weight)
    clf.fit(X_train, y_train, sample_weight=weight_train)
    return (median*metrics.confusion_matrix(y_test, clf.predict(X_test), sample_weight=weight_test), 
        metrics.confusion_matrix(y_test, clf.predict(X_test)), class_weight)

metrics_list = ['accuracy', 'f1-score', 'auroc', 'precision', 'sensitivity', 'specificity']

# for m in metrics_list:
#     print(m, ': ', performance(clf, X_test, y_test, metric=m, sample_weight=weight_test))
# print('\n\n')

result = Parallel(n_jobs=8)(delayed(fit)(class_weight={-1: 1.7 + i/80, 1: 1}) for i in tqdm(range(8)))

for r in result:
    print(r[2])
    print(r[1])
    print(r[0])
    print('\n\n')
# if kernel == 'linear':
#     print(list(zip(feature_lists, clf.coef_[0].tolist())))
#     print('\n\n')


# save_to_pickle(kernel + '.pickle', clf)