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
with open(os.path.join(APP_ROOT, '../data/new_comment_results.json')) as myfile:
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
#lexicon.create_category("silly",["silly","ridiculous","childish"])
lexicon.create_category("stupid",["stupid", "dumb","pointless", "wrong"])
#lexicon.create_category("good", ["good", "great", "perfect", "wonderful", "fantastic"]) 
lexicon.create_category("bad",["bad", "wrong", "waste", "inaccurate", "stupid", "disagree", "sad"])
lexicon.create_category("useful", ["good", "function", "effective", "interesting"])
lexicon.create_category("appreciated", ["appreciate", "thanks", "good", "useful"])
#lexicon.create_category("interesting", ["cool", "interesting", "fascinating"])
lexicon.create_category("factual", ["fact", "check", "statistics", "information", "informative"])
lexicon.create_category("shocking", ["shocked", "wtf", "shit", "jesus", "christ", "yikes"])

# def queryAnalysis(input_query):
# 	# initialize with our own categories
# 	# get empath categories from query
# 	query_sentiment = lexicon.analyze(input_query.lower(), normalize=True)
# 	relevant_query_topics = {k: v for k, v in query_sentiment.items() if v > 0}
# 	return relevant_query_topics
def queryAnalysis(query, query_sentiment):
	identical_cat_weight = 2.0
	generic_boost = 1.0

	query_topics = {k: v for k, v in query_sentiment.items() if v > 0}

	# to be returned
	cat_weights = {k: (v+generic_boost) for k, v in query_sentiment.items() if v > 0}

	# go through each word to check if topic 
	for word in query.split():
		if word in user_sentiment.keys():
			cat_weights[word] = cat_weights.get(word, 0.) + identical_cat_weight


	if 'bot' in cat_weights.keys():
		del cat_weights['bot']

	return cat_weights
def commentAnalysis(query_topics):


	# if we get categories from query, show results; otherwise show error
	if len(query_topics.items()) > 0:
		top_results = {}
		top_results['results'] = []

		
		for topic, score in query_topics.items():
			# pull top 10 results for that topic; multiply score by query weight 
			#weighted_topic_ranking =  [ (b, s * score, x, y) for (b, s, x, y) in user_sentiment[topic][-10:] ]
			weighted_topic_ranking =  [ (b, s * score, x, y) for (b, s, x, y) in user_sentiment[topic] ]

			# add to unordered list of top rankings
			top_results['results'] += weighted_topic_ranking

			# store ranking for this specific score
			top_results[topic] = weighted_topic_ranking


		
		# check if multiple categories/topics
		if len(query_topics.items()) > 1:

			# remake results and add together any duplicates
			totals = {}
			#print(top_results['results'])
			for name, v, x, y in top_results['results']:
				totals[name] = totals.get(name, (0., 0, 0.))
				totals[name] = (totals[name][0] + v, totals[name][1] + x, totals[name][2] + y)


			totals_list = map(list, totals.items())

			# sort again since we combined multiple categories 
			re_sorted_by_score = sorted(totals_list, key=lambda tup: tup[1])
			#top_results['results'] = list(reversed(re_sorted_by_score[-5:]))
			top_results['results'] = list(reversed(re_sorted_by_score))


		bot_stuff = {}
		for cat, catlist in top_results.items():
			if cat != 'results':
				for bot, score, y, z in catlist:
					placeholder = bot_stuff.get(bot, [])
					bot_stuff[bot] =  placeholder + [(cat, score)]


		for bot in bot_stuff.keys():
			thing = list(reversed(sorted(bot_stuff[bot], key=lambda tup: tup[1])))
			bot_stuff[bot] = thing


		
		# if one topic, it's already been sorted in preprocessing
		return top_results['results'], bot_stuff
	else: 
		print("no relevant categories found")
		return {}
# def commentAnalysis(query_topics, json_file):

# 	# get empath results from pickle file
# 	# 	with open(pickle_file, 'rb') as fp:
# 	# 	    user_sentiment = cpickle.load(fp)
	
# 	# cPickle.load( open(os.path.join(APP_ROOT, ('../data/' + pickle_file)), "rb" ) )
	
# 	# use json instead:

# 	# if we get categories from query, show results; otherwise show error
# 	if len(query_topics.items()) > 0:

# 		# find top 10 results for each query topic
# 		top_results = []
# 		for topic, key in query_topics.items():
# 			top_results += user_sentiment[topic]

# 		# sort again if we combined multiple categories 
# 		if len(query_topics.items()) > 1:
# 			re_sorted_by_score = sorted(top_results, key=lambda tup: tup[1])
# 			return list(reversed(re_sorted_by_score))
		
# 		# if one category, it's already been sorted in preprocessing
# 		return top_results

# 	else: 
# 		# no relevant categories found 
# 		return []
def bot_to_list(query, query_type, category):
	if query == None:
		return []	
	if category != "no category":
		category_list = user_sentiment[category]
		category_names = []
		for bot in category_list:
			category_names.append(bot[0])

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
			if category == "no category":
				data.append(entry_dict)
			elif edit_dist[i][1] in category_names:
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
			if category == "no category":
				data.append(entry_dict)
			elif cos_sim[i][0] in category_names:
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
		query_sentiment = lexicon.analyze(query, normalize=True)
		query_topics = queryAnalysis(query, query_sentiment)


		# if len(cat_weights) > 0:
		# 	output, bot_stuff = userCommentAnalysisBreakdown(cat_weights, 'user_comment_results_v1.json') #'user_sentiment.json')

		# 	if len(output) > 0:



		# 		print('\nRESULTS: ')
		# 		for thing in output:
		# 			print('\n')
		# 			print(thing)
		# 			print(bot_stuff[thing[0]])

		# else: 
		# 	print("no relevant categories found")

		myresults, stuff = commentAnalysis(query_topics)

		if not myresults:
			myresults = [("no category",0) , ("no category",0) , ("no category",0) , ("no category",0) , ("no category", 0)]
			stuff = {}

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
			res_dict["stuff"] = stuff[myresults[i][0]]
			res_dict["link"] = "http://reddit.com/u/"+ myresults[i][0]
			res_dict["category"] = "user_comments"
			entry_dict["result"] = res_dict
			if category == "no category":
				data.append(entry_dict)	
			elif myresults[i][0] in category_names:
				data.append(entry_dict)	
	return data


