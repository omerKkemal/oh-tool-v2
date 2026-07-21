'''
This file is part of the OpenHack-Tool project.
Copyright (C) 2023 OpenHack-Tool Developers <omerkemal2019@gmail.com>
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
future-proofing: This code is designed to be compatible with Python 3.x and uses modern Python features.
This file is part of the OpenHack-Tool project.
This file contains the public routes for the SpecterPanel application.
It includes routes for the home page, about page, future features,
login, registration, and logout functionalities.
It uses Flask's Blueprint to organize the routes and render templates.

Routes:
    - '/' : Home page
    - '/about' : About page
    - '/future' : Future features page
    - '/login' : Login page (GET and POST)
    - '/register' : Registration page (GET and POST)
    - '/documentation' : API documentation page
    - '/logout' : Logout route
'''

import random
import traceback
import bcrypt
from flask import Blueprint,request,render_template,redirect,url_for,session,flash
from sqlalchemy.orm import sessionmaker

from db.modle import SESSION_LOGIN, Users,ApiToken
from db.mange_db import _create_engine,config
from utility.processer import getlist,log,update_socket_info, email_optimize
from utility.email_temp import EmailTemplate


SessionLocal = sessionmaker(
    bind=_create_engine(),
    autocommit=False,
    autoflush=False
)

public = Blueprint(
    config.BLUEPRINT_NAME[2],
    __name__, template_folder='templates',
    static_folder='static', static_url_path=config.STATIC_URL_PATH
)

def SESSION(user_email, flage, session_id=None):
    _session = SessionLocal()
    if flage == 'delete':
        if session_id is None:
            return False
        _session.query(SESSION_LOGIN).filter_by(
            email=user_email,
            session_id=session_id
        ).delete()
        _session.commit()
        return True
    elif flage == 'create':
        new_session = SESSION_LOGIN(
            ID=config.ID(10), 
            email=user_email, 
            session_id=session_id or config.ID(20)
        )
        _session.add(new_session)
        _session.commit()
        _session.close()
        return True
    elif flage == 'check':
        if session_id is None:
            return False
        is_login = _session.query(SESSION_LOGIN).filter_by(
            email=user_email,
            session_id=session_id
        ).first()
        if is_login:
            return True
        else:
            return False
    else:
        return False

# home page
@public.route('/')
def index():
    try:
        return render_template('public/index.html')
    except Exception as e:
        log(f'[ERROR ROUT] : {request.endpoint} error: {e}\n{traceback.format_exc()}')
        return redirect(url_for('event.page_404'))
# about page
@public.route('/about')
def about():
    try:
        return render_template('public/about.html')
    except Exception as e:
        log(f'[ERROR ROUT] : {request.endpoint} error: {e}\n{traceback.format_exc()}')
        return redirect(url_for('event.page_404'))

# functionality under development
@public.route('/future')
def future():
    try:
        return render_template('public/future.html')
    except Exception as e:
        log(f'[ERROR ROUT] : {request.endpoint} error: {e}\n{traceback.format_exc()}')
        return redirect(url_for('event.page_404'))

# login page
@public.route('/login',methods=['GET','POST'])
def login():
    _session = SessionLocal()
    if request.method == 'GET':
        return render_template('public/login.html')
    elif request.method == 'POST':

        email = request.form["email"]
        password = request.form["password"]
        try:
            user = _session.query(Users).filter(Users.email==email).first()
            if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                session['logged'] = True
                session['email'] = email
                SESSION(email, 'create')
                __session = _session.query(SESSION_LOGIN).filter_by(email=email).first()
                session['session_id'] = __session.session_id
                flash('login successful')
                return redirect(url_for('view.dashboard'))
            else:
                flash('incorrect password or email')
                return redirect(url_for('public.login'))
        except Exception as e:
                _session.rollback()
                log(f'[ERROR ROUT] : {request.endpoint} error: {e}\n{traceback.format_exc()}')
                return str(e)

# sign up page
@public.route('/register',methods=['GET','POST'])
def register():

    _session = SessionLocal()
    if request.method == 'GET':
        return render_template('public/register.html')
    elif request.method == 'POST':
        email = request.form["email"]
        password = request.form["password"]
        con_password = request.form["con-password"]
        try:
            if password != con_password:
                flash("passwords do not match")
                return redirect(url_for('public.register'))
            token = config.ID(n=200)
            user = Users(
                email=email,
                password=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            )

            apitokn = ApiToken(config.ID(),token,email)
            _session.add(user)
            _session.add(apitokn)
            update_socket_info(token,'offline')
            # emailTemplate.sendEmail('New user',emailTemplate.new_user(email),config.ADMIN_EMAIL)
            flash('registration successful, please login')
            # # andmin notification email
            # print(email_optimize(email, request.url_root, 'new_user'))
            # # user panding email(under review)
            # print(email_optimize(email, request.url_root, 'panding'))
            # print(request.url)
            _session.commit()
            return redirect(url_for('public.login'))
        except Exception as e:
            _session.rollback()
            log(f'[ERROR ROUT] : {request.endpoint} error: {e}\n{traceback.format_exc()}')
            flash('An error occurred during registration. Please try again.')
            return str(e)

# api documentation page
@public.route("/documentation")
def documentation():
    try:
        return render_template('public/doc.html')
    except Exception as e:
        log(f'[ERROR ROUT] : {request.endpoint} error: {e}\n{traceback.format_exc()}')
        return redirect(url_for('event.page_404'))

# logout route
@public.route('/logout', methods=['GET'])
def logout():
    if "email" in session:
        SESSION(session['email'], 'delete', session.get('session_id'))
        session.clear()
        flash('logout successfully')
        return redirect(url_for("public.login"))
    else:
        flash('you need to login first')
        return redirect(url_for('public.login'))
    


@public.route('/howto')
def howto():
    try:
        return render_template('public/howto.html')
    except Exception as e:
        log(f'[ERROR ROUT] : {request.endpoint} error: {e}\n{traceback.format_exc()}')
        return redirect(url_for('event.page_404'))
