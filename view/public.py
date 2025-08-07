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
'''

import traceback
import bcrypt
from flask import Blueprint,request,render_template,redirect,url_for,session,flash
from sqlalchemy.orm import sessionmaker

from db.modle import Users,ApiToken
from db.mange_db import _create_engine,config
from utility.processer import getlist,log,update_socket_info
from utility.email_temp import email_temp

emailTemplate = email_temp()


Session = sessionmaker(bind=_create_engine())
_session = Session()

public = Blueprint('public',__name__,template_folder='templates',static_folder='static',static_url_path='/static')


@public.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        log(f'[ERROR ROUT] : {request.endpoint} error: {e}\n{traceback.format_exc()}')
        return redirect(url_for('event.404'))

@public.route('/about')
def about():
    try:
        return render_template('about.html')
    except Exception as e:
        log(f'[ERROR ROUT] : {request.endpoint} error: {e}\n{traceback.format_exc()}')
        return redirect(url_for('event.404'))


@public.route('/future')
def future():
    try:
        return render_template('future.html')
    except Exception as e:
        log(f'[ERROR ROUT] : {request.endpoint} error: {e}\n{traceback.format_exc()}')
        return redirect(url_for('event.404'))


@public.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':

        email = request.form["email"]
        password = request.form["password"]
        try:
            user = _session.query(Users).filter(Users.email==email).first()
            if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                session['email'] = email
                return redirect(url_for('view.dashboard'))
            else:
                flash('incorrect password or email')
                return redirect(url_for('public.login'))
        except Exception as e:
                _session.rollback()
                log(f'[ERROR ROUT] : {request.endpoint} error: {e}\n{traceback.format_exc()}')


@public.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
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
            _session.commit()
            # emailTemplate.sendEmail('New user',emailTemplate.new_user(email),config.ADMIN_EMAIL)
            return redirect(url_for('public.login'))
        except Exception as e:
            _session.rollback()
            log(f'[ERROR ROUT] : {request.endpoint} error: {e}\n{traceback.format_exc()}')
            flash('An error occurred during registration. Please try again.')
            return str(e)

@public.route('/logout', methods=['POST'])
def logout():
    if "email" in session:
        session.pop("email", None)
        flash('logout successfully')
        return redirect(url_for("public.login"))
    else:
        flash('you need to login first')
        return redirect(url_for('public.login'))
    

@public.route('/test')
def test():
    return render_template('test.html')