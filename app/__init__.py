from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Create Flask application instance
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hello123456789000'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///info_database.db'

# Initialize SQLAlchemy
db = SQLAlchemy(app)
app.app_context().push()

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Import your views and models here
from app import routes, models

