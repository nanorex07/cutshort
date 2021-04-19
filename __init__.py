from flask import Flask, redirect, url_for, session
from .dbm import DBManager
from functools import wraps
import string, random

db = DBManager()
BASE_URL = "http://0.0.0.0:5000/url/"
def login_required(f):
    @wraps(f)
    def dec_func(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect((url_for('auth.login')))
        return f(*args, **kwargs)
    return dec_func

def random_str(length=4):
    s = ''
    for i in range(length):
        s += random.choice(string.ascii_lowercase+string.ascii_uppercase+string.digits)
    return s

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'CutShort'

    from .auth import auth
    app.register_blueprint(auth, url_prefix='/')
    from .views import views
    app.register_blueprint(views, url_prefix='/')
    
    return app