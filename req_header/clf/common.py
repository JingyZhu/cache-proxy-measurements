import os
from sklearn import metrics
from urllib.parse import urlparse
import pickle
import json
import numpy as np

cacheable_ext = ['.png', '.jpeg', '.jpg', '.ttf', 'woff2', '.svg', 'js']
uncacheable_ext = ['.gif', '.php', '.aspx', 'ashx', '']
feature_lists = ['cdn/asset', 'Font', 'Image', 'Script', 'cache_ext',  \
                'isnotGET', 'XHR', 'Query', 'Document', 'Uncache_ext', 'content-type/content-length', \
                'cookie', 'host', 'connection', ':path']

def get_feature_vector(req):
    ext = os.path.splitext(urlparse(req['url']).path)[1]
    ext = ext.lower()
    has_headers = 'headers' in req
    if has_headers:
        req['headers'] = {header.lower(): value for header, value in req['headers'].items()}
    rlist = ['cdn' in req['url'] or 'asset' in req['url'], \
            req['type'] == 'Font', \
            req['type'] == 'Image', \
            req['type'] == 'Script', \
            ext in cacheable_ext, \
            req['method'] != 'GET', \
            req['type'] == 'XHR', \
            urlparse(req['url']).query != '', \
            req['type'] == 'Document', \
            ext in uncacheable_ext, \
            has_headers and ('content-type' in req['headers'] or 'content-length' in req['headers']), \
            has_headers and 'cookie' in req['headers'], \
            has_headers and 'host' in req['headers'], \
            has_headers and 'connection' in req['headers'], \
            has_headers and ':path' in req['headers']]
    return list(map(int, rlist))

def performance(clf_trained, X, y, metric='accuracy', sample_weight=None):
    precision = lambda cm: cm[1][1] / (cm[1][1] + cm[0][1])
    sensitivity =  lambda cm: cm[1][1] / (cm[1][1] + cm[1][0])
    todos1 = {
        'auroc' : metrics.roc_auc_score
    }
    todos2 = {
        'accuracy': lambda cm: (cm[1][1] + cm[0][0])/ y.shape[0],
        'precision': precision,
        'sensitivity': sensitivity,
        'specificity': lambda cm: cm[0][0] / (cm[0][0] + cm[0][1]),
        'f1-score': lambda cm:  2*precision(cm)*sensitivity(cm) / (precision(cm)+sensitivity(cm)) # 2TP / (2TP + FN + FP)
    }
    if metric in ['auroc']:
        y_test = clf_trained.predict(X)
        return todos1[metric](y, y_test)
    else:
        y_test = clf_trained.predict(X)
        if sample_weight is not None:
            cm = metrics.confusion_matrix(y, y_test, labels=[-1,1], sample_weight=sample_weight)
        else:
            cm = metrics.confusion_matrix(y, y_test, labels=[-1,1])
        return todos2[metric](cm)


def save_to_pickle(filename, clf):
    with open(filename, 'wb') as f:
        pickle.dump(clf, f)


def load_from_file(filename):
    with open(filename, 'rb') as f:
        clf = pickle.load(f)
        return clf
    raise NotImplementedError


def get_dataset():
    X, y = [], []
    cacheable_list = os.listdir('../headers/cacheable')
    uncacheable_list = os.listdir('../headers/uncacheable')
    for cache_file in cacheable_list:
        cache_file = os.path.join('..', 'headers', 'cacheable', cache_file)
        file = open(cache_file, 'r', encoding='utf-8').read()
        cache_json = json.loads(file)
        for req in cache_json.values():
            X.append(get_feature_vector(req))
            y.append(1)

    for uncache_file in uncacheable_list:
        uncache_file = os.path.join('..', 'headers', 'uncacheable', uncache_file)
        file = open(uncache_file, 'r', encoding='utf-8').read()
        uncache_json = json.loads(file)
        for req in uncache_json.values():
            X.append(get_feature_vector(req))
            y.append(-1)
    return (np.array(X), np.array(y))

def get_weighted_dataset():
    X, y, weights = [], [], []
    cacheable_list = os.listdir('../headers/cacheable')
    uncacheable_list = os.listdir('../headers/uncacheable')
    for cache_file in cacheable_list:
        cache_file = os.path.join('..', 'headers', 'cacheable', cache_file)
        file = open(cache_file, 'r', encoding='utf-8').read()
        cache_json = json.loads(file)
        for req in cache_json.values():
            X.append(get_feature_vector(req))
            y.append(1)
            byte = req['bytes'] if 'bytes' in req else 1
            weights.append(byte)

    for uncache_file in uncacheable_list:
        uncache_file = os.path.join('..', 'headers', 'uncacheable', uncache_file)
        file = open(uncache_file, 'r', encoding='utf-8').read()
        uncache_json = json.loads(file)
        for req in uncache_json.values():
            X.append(get_feature_vector(req))
            y.append(-1)
            byte = req['bytes'] if 'bytes' in req else 1
            weights.append(byte)
    
    weights = np.array(weights)
    median = np.median(weights)
    weights = weights / median
    return (np.array(X), np.array(y), np.array(weights), median)