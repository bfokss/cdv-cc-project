from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
try:
    import project.Config as Config
except:
    print("You need to create Config.py file in the root directory!")
    exit()

app = Flask(__name__)
api = Api(app)

try:
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.CONNECTION_STRING
except:
    print("Your Config class doesn't contain the CONNECTION_STRING const!")
    exit()

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)