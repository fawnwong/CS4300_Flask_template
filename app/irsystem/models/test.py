import Levenshtein  # package python-Levenshtein
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from empath import Empath
import json
import os
import csv
import re
import cPickle

APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
#with open(os.path.join(APP_ROOT, '../data/data.json')) as f:
#	bot_data = json.loads(f.readlines()[0])
bot_data  = cPickle.load( open(os.path.join(APP_ROOT, '../data/bot_data.p'), "rb" ) )


botname_to_index = {botname:index for index, botname in enumerate(bot_data.keys())}
index_to_botname = {v:k for k,v in botname_to_index.items()}

tfidf_vec = cPickle.load( open(os.path.join(APP_ROOT, '../data/vectorizer.p'), "rb" ) )
#reply_tfidf_vec = cPickle.load( open(os.path.join(APP_ROOT, '../data/replyvectorizer.p'), "rb" ) )
#doc_by_vocab = cPickle.load( open(os.path.join(APP_ROOT, '../data/doc_by_vocab.p'), "rb" ) )

doc_by_vocab = tfidf_vec.transform([bot_data[d] for d in bot_data.keys()]).toarray()

np.save( open(os.path.join(APP_ROOT, '../data/doc_by_vocab.p'), "wb" ), doc_by_vocab, allow_pickle = True, fix_imports = True)
np_doc = np.load(open(os.path.join(APP_ROOT, '../data/doc_by_vocab.p'), "rb" ), allow_pickle = True, fix_imports = True)

def top_n_cos_real(n,query_string, tfidf):
	q_vec = tfidf.transform([query_string]).toarray()
	cosines = np.array([np.dot(q_vec, d) for d in doc_by_vocab]).T[0]
	args = np.argsort(cosines)[::-1][:n]
	return [(index_to_botname[x], bot_data[index_to_botname[x]]) for x in args]

def top_n_cos_np(n,query_string, tfidf):
	q_vec = tfidf.transform([query_string]).toarray()
	cosines = np.array([np.dot(q_vec, d) for d in np_doc]).T[0]
	args = np.argsort(cosines)[::-1][:n]
	return [(index_to_botname[x], bot_data[index_to_botname[x]]) for x in args]

print("real ----- ")
print(top_n_cos_real(1, "gif edit", tfidf_vec))
print("NP --------")
print(top_n_cos_np(1, "gif edit", tfidf_vec))
