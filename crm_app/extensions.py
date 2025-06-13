from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect() # Initialize CSRFProtect

login_manager.login_view = 'auth.login' # Assuming auth blueprint and login route name
login_manager.login_message_category = 'info' # Optional: for styling flashed messages
