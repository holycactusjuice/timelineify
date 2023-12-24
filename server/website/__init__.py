from flask import Flask
from flask_login import LoginManager
from pymongo import MongoClient
from flask_pymongo import PyMongo


CLIENT_ID = "88405b10e1704946976efdef33e73f64"
CLIENT_SECRET = "9f5d2959d24e461a9b64b7a38291c0cf"
REDIRECT_URI = "http://localhost:5000/callback"
MONGODB_PASSWORD = "FPurGYkgNlzLrVPQ"
MONGODB_USERNAME = "pat-2"
DB_NAME = "Timelineify"


client = MongoClient(
    f'mongodb+srv://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@cluster0.t4brvzm.mongodb.net/test?retryWrites=true&w=majority')
db = client[DB_NAME]
users = db['users']
trakcs = db['tracks']


def create_app():
    app = Flask(__name__)
    app.config['MONGO_URI'] = f'mongodb://localhost:27017/{DB_NAME}'

    mongo = PyMongo()
    mongo.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        user_document = users.find_one(
            {'_id': ObjectId(user_id)})
        if user_document:
            return User.from_document(user_document)
        else:
            return None

    return app