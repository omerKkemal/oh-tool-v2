from flask import Blueprint,request,render_template,redirect,url_for,session,flash
from sqlalchemy.orm import sessionmaker

from db.modle import Users,ApiToken
from db.mange_db import _create_engine,config
from utility.processer import getlist,sendEmail,log
from utility.email_temp import email_temp

emailTemplate = email_temp()

Session = sessionmaker(bind=_create_engine())
_session = Session()

public = Blueprint('public',__name__,template_folder='templates',static_folder='static',static_url_path='/static')


@public.route('/')
def index():
    return render_template('index.html')


@public.route('/about')
def about():
    return render_template('about.html')


@public.route('/future')
def future():
    return render_template('future.html')


@public.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':

        email = request.form["email"]
        password = request.form["password"]
        try:
            user = _session.query(Users).filter(Users.email==email,Users.password==password).first()
            if user:
                session['email'] = email
                return redirect(url_for('view.profile'))
            else:
                flash('incorrect password or email')
                return redirect(url_for('public.login'))
        except Exception as e:
                log(f'[ERROR ROUT] : {request.endpoint} error: {e}')


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
            user = Users(email=email,password=password)
            apitokn = ApiToken(config.ID(),config.ID(n=200),email)
            _session.add(user)
            _session.add(apitokn)
            _session.commit()
            # sendEmail('New user',emailTemplate.new_user(email),config.ADMIN_EMAIL)
            return redirect(url_for('public.login'))
        except Exception as e:
            return str(e)

@public.route('/logout')
def logout():
    if "userID" in session:
        session.pop("userID",None)
        session.pop("role",None)
        session.pop("username",None)
        flash('logout succsessfully')
        return redirect(url_for("public.login"))
    else:
        flash('you need to login first')
        return redirect(url_for('public.login'))
    

@public.route('/test')
def test():
    return render_template('test.html')