import time
from flask import Flask, Response, g, jsonify, render_template, request
from flask_login import LoginManager, login_required
from dotenv import load_dotenv
import os

load_dotenv()

ENV_DB_PATH = os.getenv('DB_PATH')
ENV_SQLALCHEMY_ECHO = os.getenv('SQLALCHEMY_ECHO') == "1"

dbPath = os.path.abspath(ENV_DB_PATH)

app = Flask(__name__)

app.secret_key = 'SECRET_KEY'
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{dbPath}"
app.config["SQLALCHEMY_ECHO"] = ENV_SQLALCHEMY_ECHO
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

from common import db
from models import *

db.init_app(app)
app.app_context().push()

login_manager = LoginManager()
login_manager.init_app(app) 
@login_manager.user_loader
def load_user(user_id):
    return CurrentUser(user_id)

#routers
from blueprints.category import category
from blueprints.auth import auth
app.register_blueprint(blueprint=auth)
app.register_blueprint(blueprint=category)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/protected')
@login_required
def protected():
    return render_template('protected.html')

@app.errorhandler(404)
def not_found(e):
    return render_template("index.html")

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({"error": "Unauthorized"}), 401

@app.before_request
def before_request():
    g.start_time = time.time()

@app.after_request
def after_request(response):
    g.end_time = time.time()
    print(f"{request.path} took {g.end_time - g.start_time}s")
    return response

if __name__ == '__main__':
    app.run(debug=True, port=8002)
