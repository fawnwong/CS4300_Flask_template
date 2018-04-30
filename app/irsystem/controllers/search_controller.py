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
	query_filter = request.args.get('search-filter')
	if query_filter == "none":
		query_filter = "no category"
	if query == None:
		data = []
		output_message = 'No results found.'
	else:
		output_message = "Search results: "
		# data should be a list of dictionaries d for now, in decreasing order of importance
		# each dictionary d has a rank field and a list of results, e, of that rank for the three search categories
		# for now make sure to define the list e in the order of bot name, bot comment, user comment searches
		# each element in list e is a dictionary representing a result

		#replace no category with a category variable
		# lexicon.create_category("funny",["funny","lol","hilarious", "haha", "joke"])
		# lexicon.create_category("stupid",["stupid", "dumb","pointless", "wrong"])
		# lexicon.create_category("bad",["bad", "wrong", "waste", "inaccurate", "stupid", "disagree", "sad"])
		# lexicon.create_category("useful", ["good", "function", "effective", "interesting"])
		# lexicon.create_category("appreciated", ["appreciate", "thanks", "good", "useful"])
		# lexicon.create_category("factual", ["fact", "check", "statistics", "information", "informative"])
		# lexicon.create_category("shocking", ["shocked", "wtf", "shit", "jesus", "christ", "yikes"])
		data = bot_to_list(query, query_type, query_filter)
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)



