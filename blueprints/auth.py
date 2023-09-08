import uuid
from flask import Blueprint, abort, request, render_template, redirect, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from common import db, measure
from models import CurrentUser, Login, Role, User, UserRole

auth = Blueprint(name='auth', url_prefix="/api/auth", import_name=__name__)
  

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
       
        user:User = db.session.query(User).filter_by(login_id=login.id).first()
        if user is None:
            abort(401)

        currentUser = CurrentUser(user.id)
        if(login_user(currentUser)):
            return {'success': True }
            # return redirect(url_for('protected'))

        abort(401)
    else:
        return render_template('auth/login.html')

@auth.route('/logout')
def logout():
    logout_user()
    # return redirect(url_for('index'))
    return {'success': True }

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username:str = request.form['username']
        password:str = request.form['password']
        passwordHash = generate_password_hash(password)
        login_id:str = str(uuid.uuid4())

        #create a login
        login = Login(id=login_id, userName=username, normalizedUserName=username.upper(), passwordHash=passwordHash)
        db.session.add(login)

        #add a user to it
        user_id:str = str(uuid.uuid4())
        user = User(id=user_id, login_id=login_id, name=login.userName, email=login.userName)
        db.session.add(user)

        #get default role
        adminRole:Role = db.session.query(Role).filter_by(code="ADMIN").first()
        
        #assign default role to the user
        userRole = UserRole(id=str(uuid.uuid4()), user_id=user.id, role_id=adminRole.id)
        db.session.add(userRole)
        db.session.commit()

        currentUser = CurrentUser(user.id)
        if(login_user(currentUser)):
            return {'success': True }
    else:
        return render_template('auth/register.html')