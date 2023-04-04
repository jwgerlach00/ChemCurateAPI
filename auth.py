from flask import Blueprint, redirect, url_for, request, make_response
from werkzeug.security import check_password_hash
from flask_login import login_user, login_required, current_user, logout_user
from flask import session

from db import user_db, User


auth = Blueprint('auth', __name__)


# --------------------------------- REDIRECTS -------------------------------- #
@auth.route('/login_failed', methods=['GET'])
def login_failed():
    return 'login_failed', 401

@auth.route('/exists', methods=['GET'])
def exists():
    return 'user_exists', 409


# ---------------------------------- ROUTES ---------------------------------- #
@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username, pw = data['username'], data['password']
    
    user = User.query.filter_by(username=username).first()
    
    if not user or not check_password_hash(user.password, pw):
        return redirect(url_for('auth.login_failed'))
    else:
        login_user(user, remember=False)
        session['username'] = data['username']
        
        print('login', current_user.is_authenticated)

        return 'login_success', 204
    
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return 'logout_success', 204

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username, pw = data['username'], data['password']

    if User.query.filter_by(username=username).first():
        return redirect(url_for('auth.exists'))
    else:
        user_db.add_user(username, pw)

    return 'register_success', 204

@auth.route('/is_authenticated', methods=['GET'])
def is_authenticated():
    return ('yes', 204) if current_user.is_authenticated else ('no', 401)
