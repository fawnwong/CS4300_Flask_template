from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder

project_name = "beepboop: Bot Finder"
net_id = "Fawn Wong (fyw6), Cindy Wang (cw653), Danna Greenberg (dg489), Stephanie Hogan (sjh278), Annie Zhang (zz229)"

@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search')
	if not query:
		data = []
		output_message = ''
	else:
		output_message = "Search results: "
		# data should be a list of dictionaries for now, in decreasing order of importance
		# limit length to 5 and have a name, comment, and link field for each
		data = [
			{"name": "Bot 1", "comment": "Comment 1", "link": "http://www.google.com"},
			{"name": "Bot 2", "comment": "Comment 2", "link": "http://www.google.com"},
			{"name": "Bot 3", "comment": "Comment 3", "link": "http://www.google.com"},
			{"name": "Bot 4", "comment": "Comment 4", "link": "http://www.google.com"},
			{"name": "Bot 5", "comment": "Comment 5", "link": "http://www.google.com"}
		]
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)



