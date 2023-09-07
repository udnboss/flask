from flask import Flask, Response, jsonify, render_template
from flask_login import LoginManager, login_required

app = Flask(__name__)

app.secret_key = 'SECRET_KEY'
app.config["SQLALCHEMY_DATABASE_URI"] = r"sqlite:///D:\Dev\flask\db\db.sqlite3"
app.config["SQLALCHEMY_ECHO"] = True
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
app.register_blueprint(blueprint=auth, url_prefix="/auth")
app.register_blueprint(blueprint=category, url_prefix="/category")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/protected')
@login_required
def protected():
    return render_template('protected.html')

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({"error": "Unauthorized"}), 401

if __name__ == '__main__':
    app.run(debug=True, port=8002)
