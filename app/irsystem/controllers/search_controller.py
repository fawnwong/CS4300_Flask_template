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
		output_message = "Your search: " + query
		data = range(5)
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)



