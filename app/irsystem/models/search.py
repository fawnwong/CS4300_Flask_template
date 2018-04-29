import Levenshtein  # package python-Levenshtein
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from empath import Empath
import json
import os
import csv
import re
import cPickle
import urllib

APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top

bot_data  = cPickle.load( open(os.path.join(APP_ROOT, '../data/bot_data.p'), "rb" ) )

# result_dict = cPickle.load( open(os.path.join(APP_ROOT, '../data/user_results.p'), "rb" ) )
with open(os.path.join(APP_ROOT, '../data/user_sentiment.json')) as myfile:
	user_sentiment = json.loads(myfile.read())

bot_names = bot_data.keys()
botname_to_index = {botname:index for index, botname in enumerate(bot_data.keys())}
index_to_botname = {v:k for k,v in botname_to_index.items()}

n_feats = 2000
doc_by_vocab = np.empty([len(bot_data), n_feats])

	
tfidf_vec = cPickle.load( open(os.path.join(APP_ROOT, '../data/vectorizer.p'), "rb" ) )

doc_by_vocab = np.load(open(os.path.join(APP_ROOT, '../data/doc_by_vocab.p'), "rb" ), encoding="latin1",allow_pickle = True, fix_imports = True)
# doc_by_vocab = tfidf_vec.transform([bot_data[d] for d in bot_data.keys()]).toarray()

def top_n_cos(n,query_string, tfidf):
	q_vec = tfidf.transform([query_string]).toarray()
	cosines = np.array([np.dot(q_vec, d) for d in doc_by_vocab]).T[0]
	args = np.argsort(cosines)[::-1][:n]
	return [(index_to_botname[x], bot_data[index_to_botname[x]]) for x in args]

def edit_distance(query_str, msg_str):
	return Levenshtein.distance(query_str.lower(), msg_str.lower())


def similar_names(query, msgs):
	li = [(edit_distance(query, msg),msg) for msg in msgs]
	li.sort(key=lambda x: x[0])
	return li[0:5]

lexicon = Empath()
lexicon.create_category("funny",["funny","lol","hilarious", "haha", "joke"])
#lexicon.create_category("silly",["silly","dumb","ridiculous", "stupid", "childish", "fun"])
lexicon.create_category("stupid",["stupid","dumb","pointless", "why", "wrong"])
lexicon.create_category("good", ["good", "great", "wonderful", "fantastic", "useful", "appreciated"])
lexicon.create_category("bad",["bad", "wrong", "inaccurate", "stupid", "disagree"])
lexicon.create_category("useful", ["good", "function", "effective", "interesting", "learn"])
lexicon.create_category("appreciated", ["appreciate", "thanks", "good", "useful"])
#lexicon.create_category("interesting", ["cool", "interesting", "fascinating"])
lexicon.create_category("moderating", ["moderating", "mod", "moderate", "rules", "comment", "removed"])
lexicon.create_category("factual", ["fact", "check", "statistics", "information", "informative"])

def queryAnalysis(input_query):
	# initialize with our own categories
	# get empath categories from query
	query_sentiment = lexicon.analyze(input_query.lower(), normalize=True)
	relevant_query_topics = {k: v for k, v in query_sentiment.items() if v > 0}
	return relevant_query_topics

def commentAnalysis(query_topics, json_file):

	# get empath results from pickle file
	# 	with open(pickle_file, 'rb') as fp:
	# 	    user_sentiment = cpickle.load(fp)
	
	# cPickle.load( open(os.path.join(APP_ROOT, ('../data/' + pickle_file)), "rb" ) )
	
	# use json instead:

	# if we get categories from query, show results; otherwise show error
	if len(query_topics.items()) > 0:

		# find top 10 results for each query topic
		top_results = []
		for topic, key in query_topics.items():
			top_results += user_sentiment[topic][-10:]

		# sort again if we combined multiple categories 
		if len(query_topics.items()) > 1:
			re_sorted_by_score = sorted(top_results, key=lambda tup: tup[1])
			return list(reversed(re_sorted_by_score[-10:]))
		
		# if one category, it's already been sorted in preprocessing
		return top_results

	else: 
		# no relevant categories found 
		return []

def bot_to_list(query, query_type):
	if query == None:
		return []
	if query_type == "name":
		edit_dist = similar_names(query, bot_names)
		data = [{"rank": "1", "result": {"name": edit_dist[0][1], "comment": "A Comment 1", "link": "http://reddit.com/u/"+ edit_dist[0][1], "category": "bot_name"}},
			{"rank": "2",
			"result":{"name": edit_dist[1][1], "comment": "A Comment 2", "link": "http://reddit.com/u/" + edit_dist[1][1], "category": "bot_name"}
					 },
			{"rank": "3",
			"result": {"name": edit_dist[2][1], "comment": "A Comment 3", "link": "http://reddit.com/u/" + edit_dist[2][1], "category": "bot_name"}
					 },
			{"rank": "4",
			"result": {"name": edit_dist[3][1], "comment": "A Comment 4", "link": "http://reddit.com/u/" + edit_dist[3][1], "category": "bot_name"}
					 },
			{"rank": "5",
			"result": {"name": edit_dist[4][1], "comment": "A Comment 5", "link":"http://reddit.com/u/" + edit_dist[4][1], "category": "bot_name"}
					 }
			]
	elif query_type == "bot-com":
		cos_sim = top_n_cos(5,query, tfidf_vec)
		data = [{"rank": "1", "result": {"name": cos_sim[0][0], "comment": "B Comment 1", "link": "http://reddit.com/u/"+cos_sim[0][0], "category": "bot_comments"}},
			{"rank": "2",
			"result":{"name": cos_sim[1][0], "comment": "B Comment 2", "link": "http://reddit.com/u/"+cos_sim[1][0], "category": "bot_comments"}
					 },
			{"rank": "3",
			"result": {"name": cos_sim[2][0], "comment": "B Comment 3", "link": "http://reddit.com/u/"+cos_sim[2][0], "category": "bot_comments"}
					 },
			{"rank": "4",
			"result": {"name": cos_sim[3][0], "comment": "B Comment 4", "link": "http://reddit.com/u/"+cos_sim[3][0], "category": "bot_comments"}
					 },
			{"rank": "5",
			"result": {"name": cos_sim[4][0], "comment": "B Comment 5", "link": "http://reddit.com/u/"+cos_sim[4][0], "category": "bot_comments"}
					 }
			]
	else:
		'''
		bot_names_list = 'bot_names.csv'
		user_comments = 'user_comment_data.csv'
		
		query_words = query.split()
		for query in query_words:
			myresults = getUserCommentResults(query, bot_names_list, user_comments)
			if myresults:
				break
		'''
		
		query_topics = queryAnalysis(query)
		myresults = commentAnalysis(query_topics, 'user_sentiment.json')

		if not myresults:
			myresults = [("no category",0) , ("no category",0) , ("no category",0) , ("no category",0) , ("no category", 0)]

		data = [{"rank": "1", "result": {"name": myresults[0][0], "comment": "C Comment 1", "link": "http://reddit.com/u/" + myresults[0][0], "category": "user_comments"}},
			{"rank": "2",
			"result":{"name": myresults[1][0], "comment": "C Comment 2", "link": "http://reddit.com/u/" + myresults[1][0], "category": "user_comments"}
					 },
			{"rank": "3",
			"result": {"name": myresults[2][0], "comment": "C Comment 2", "link": "http://reddit.com/u/" + myresults[2][0], "category": "user_comments"}
					 },
			{"rank": "4",
			"result": {"name": myresults[3][0], "comment": "C Comment 2", "link": "http://reddit.com/u/" + myresults[3][0], "category": "user_comments"}
					 },
			{"rank": "5",
			"result": {"name": myresults[4][0], "comment": "C Comment 2", "link": "http://reddit.com/u/" + myresults[4][0], "category": "user_comments"}
					 }
			]

	return data


