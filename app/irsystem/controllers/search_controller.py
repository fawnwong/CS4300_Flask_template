from . import *
from app.irsystem.models.search import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder

project_name = "beepboop: Bot Finder"
net_id = "Fawn Wong (fyw6), Cindy Wang (cw653), Danna Greenberg (dg489), Stephanie Hogan (sjh278), Annie Zhang (zz229)"

@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search')
	query_type = request.args.get('search-type')
	if query == None:
		data = []
		output_message = ''
	else:
		output_message = "Search results: "
		# data should be a list of dictionaries d for now, in decreasing order of importance
		# each dictionary d has a rank field and a list of results, e, of that rank for the three search categories
		# for now make sure to define the list e in the order of bot name, bot comment, user comment searches
		# each element in list e is a dictionary representing a result
		# data = [
		# 	{"rank": "1", 
		# 	"list": [
		# 		{"name": "A Bot 1", "comment": "A Comment 1", "link": "http://www.google.com", "category": "bot_name", "score": 1},
		# 		{"name": "B Bot 1", "comment": "B Comment 1", "link": "http://www.google.com", "category": "bot_comments", "score": 0.234},
		# 		{"name": "C Bot 1", "comment": "C Comment 1", "link": "http://www.google.com", "category": "user_comments", "score": 0.874}
		# 	]},
		# 	{"rank": "2",
		# 	"list": [
		# 		{"name": "A Bot 2", "comment": "A Comment 2", "link": "http://www.google.com", "category": "bot_name", "score": 0.436},
		# 		{"name": "B Bot 2", "comment": "B Comment 2", "link": "http://www.google.com", "category": "bot_comments", "score": 0.123},
		# 		{"name": "C Bot 2", "comment": "C Comment 2", "link": "http://www.google.com", "category": "user_comments", "score": 0.254}
		# 	]},
		# 	{"rank": "3", 
		# 	"list": [
		# 		{"name": "A Bot 3", "comment": "A Comment 3", "link": "http://www.google.com", "category": "bot_name", "score": 0.921},
		# 		{"name": "B Bot 3", "comment": "B Comment 3", "link": "http://www.google.com", "category": "bot_comments", "score": 0.452},
		# 		{"name": "C Bot 3", "comment": "C Comment 3", "link": "http://www.google.com", "category": "user_comments", "score": 0.109}
		# 	]},
		# 	{"rank": "4", 
		# 	"list": [
		# 		{"name": "A Bot 4", "comment": "A Comment 4", "link": "http://www.google.com", "category": "bot_name", "score": 0.872},
		# 		{"name": "B Bot 4", "comment": "B Comment 4", "link": "http://www.google.com", "category": "bot_comments", "score": 0.154},
		# 		{"name": "C Bot 4", "comment": "C Comment 4", "link": "http://www.google.com", "category": "user_comments", "score": 0.209}
		# 	]},
		# 	{"rank": "5", 
		# 	"list": [
		# 		{"name": "A Bot 5", "comment": "A Comment 5", "link": "http://www.google.com", "category": "bot_name", "score": 0.652},
		# 		{"name": "B Bot 5", "comment": "B Comment 5", "link": "http://www.google.com", "category": "bot_comments", "score": 0.591},
		# 		{"name": "C Bot 5", "comment": "C Comment 5", "link": "http://www.google.com", "category": "user_comments", "score": 0.194}
		# 	]},
		# ]
		data = bot_to_list(query, query_type)
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)



