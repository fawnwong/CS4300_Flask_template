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

# doc_by_vocab = np.load(open(os.path.join(APP_ROOT, '../data/doc_by_vocab.p'), "rb" ), encoding="bytes",allow_pickle = True, fix_imports = True)
doc_by_vocab = tfidf_vec.transform([bot_data[d] for d in bot_data.keys()]).toarray()

bot_info = cPickle.load( open(os.path.join(APP_ROOT, '../data/bot_info.p'), "rb" ) )


def top_n_cos(query_string, tfidf):
	q_vec = tfidf.transform([query_string]).toarray()
	cosines = np.array([np.dot(q_vec, d) for d in doc_by_vocab]).T[0]
	args = np.argsort(cosines)[::-1]
	return [(index_to_botname[x], cosines[x]) for x in args]

def edit_distance(query_str, msg_str):
	return Levenshtein.distance(query_str.lower(), msg_str.lower())


def similar_names(query, msgs):
	li = [(edit_distance(query, msg),msg) for msg in msgs]
	li.sort(key=lambda x: x[0])
	return li

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
			top_results += user_sentiment[topic]

		# sort again if we combined multiple categories 
		if len(query_topics.items()) > 1:
			re_sorted_by_score = sorted(top_results, key=lambda tup: tup[1])
			return list(reversed(re_sorted_by_score))
		
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
		data = []
		for i in range(len(edit_dist)):
			entry_dict = {}
			entry_dict["rank"] = str(i+1)
			res_dict = {}
			res_dict["name"] = edit_dist[i][1]
			(karma, score, comment) = bot_info[res_dict["name"]]
			res_dict["karma"] = karma
			res_dict["reliability"] = score
			res_dict["comment"] = comment
			res_dict["score"] = edit_dist[i][0]
			res_dict["link"] = "http://reddit.com/u/"+ edit_dist[i][1]
			res_dict["category"] = "bot_name"
			entry_dict["result"] = res_dict
			data.append(entry_dict)
	elif query_type == "bot-com":
		cos_sim = top_n_cos(query, tfidf_vec)
		data = []
		for i in range(len(cos_sim)):
			entry_dict = {}
			entry_dict["rank"] = str(i+1)
			res_dict = {}
			res_dict["name"] = cos_sim[i][0]
			(karma, score, comment) = bot_info[res_dict["name"]]
			res_dict["karma"] = karma
			res_dict["reliability"] = score
			res_dict["comment"] = comment
			res_dict["score"] = cos_sim[i][1]
			res_dict["link"] = "http://reddit.com/u/"+ cos_sim[i][0]
			res_dict["category"] = "bot_comments"
			entry_dict["result"] = res_dict
			data.append(entry_dict)

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

		data = []
		for i in range(len(myresults)):
			entry_dict = {}
			entry_dict["rank"] = str(i+1)
			res_dict = {}
			res_dict["name"] = myresults[i][0]
			(karma, score, comment) = bot_info[res_dict["name"]]
			res_dict["karma"] = karma
			res_dict["reliability"] = score
			res_dict["comment"] = comment
			res_dict["score"] = myresults[i][1]
			res_dict["link"] = "http://reddit.com/u/"+ myresults[i][0]
			res_dict["category"] = "user_comments"
			entry_dict["result"] = res_dict
			data.append(entry_dict)	

	return data


