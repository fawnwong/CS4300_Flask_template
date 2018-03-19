from flask import Blueprint

# Define a Blueprint for this module (mchat)
accounts = Blueprint('accounts', __name__, url_prefix='/accounts')

# Import all controllers
try:
	from controllers.users_controller import *
	from controllers.sessions_controller import *
except ImportError:
	from app.accounts.controllers.users_controller import *
	from app.accounts.controllers.sessions_controller import *