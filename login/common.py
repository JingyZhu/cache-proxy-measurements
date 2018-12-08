"""
Common functions for handling request/response
"""
import base64
import brotli
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def lower_headers(h):
    return {k.lower(): v for k, v in h.items()}

def strip_colon(headers):
	new_header = {}
	for k, v in headers.items():
		new_header[k.strip(':')] = v
	return new_header

def similar(len1, len2, text1, text2, thres=0.98):
    if len1 == 0 and len2 == 0 or (len1 == len2):
        return True, 1
    else: # tf-idf
        vectorizer = TfidfVectorizer()
        try:
            x = vectorizer.fit_transform([text1, text2])
            similar = cosine_similarity(x)[0][1]
        except:
            similar = 0
        return similar > thres, similar

# Tect: Whethertext should be returned
def find_length(r, text=False):
    r.hedaers = lower_headers(r.headers)
    if not text:
        if 'content-encoding' in r.headers and r.headers['content-encoding'] == 'br':
            data = brotli.decompress(r.content)
            try:
                return len(data.decode())
            except:
                return len(base64.b64encode(data).decode())
        else:
            try:
                return len(r.content.decode())
            except:
                return len(base64.b64encode(r.content).decode())
    else:
        if 'content-encoding' in r.headers and r.headers['content-encoding'] == 'br':
            data = brotli.decompress(r.content)
            try:
                return len(data.decode()), data.decode()
            except:
                return len(base64.b64encode(data).decode()), base64.b64encode(data).decode()
        else:
            try:
                return len(r.content.decode()), r.content.decode()
            except:
                return len(base64.b64encode(r.content).decode()), base64.b64encode(r.content).decode()