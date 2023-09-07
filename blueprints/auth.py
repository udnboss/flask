import uuid
from flask import Blueprint, abort, request, render_template, redirect, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from common import db
from models import CurrentUser, Login, User, UserRole

auth = Blueprint('auth', __name__)

# users = [CurrentUser(id) for id in range(1, 21)]
    
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        login:Login = db.session.query(Login).filter_by(userName=username).first()

        if login is None:
            abort(401)        
        
        if(not check_password_hash(login.passwordHash, password)):
            abort(401)
       
        u:User = db.session.query(User).filter_by(login_id=login.id).first()
        if u is None:
            abort(401)

        user = CurrentUser(u.id)
        if(login_user(user)):
            return {'success': True }
            # return redirect(url_for('protected'))

        abort(401)
    else:
        return render_template('auth/login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    # return redirect(url_for('index'))
    return {'success': True }

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        passwordHash = generate_password_hash(password)
        login = Login(id=str(uuid.uuid4()), userName=username, passwordHash=passwordHash)
        db.session.add(login)
        #add default user and roles etc.
        user = User(id=str(uuid.uuid4()), login_id=login.id, name=login.userName, email=login.userName)
        db.session.add(user)

        userRole = UserRole(id=str(uuid.uuid4()), user_id=user.id, role_id='550e8400-e29b-41d4-a716-446655440000')
        db.session.add(userRole)
        db.session.commit()
    else:
        return render_template('auth/register.html')