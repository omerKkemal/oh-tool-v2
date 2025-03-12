from flask import Flask,render_template,url_for,Blueprint,request,session,flash,redirect

from db.modle import Users,APICommand,APILink,Fishing,Hooking
from db.mange_db import config,create_engine
from utility.email_temp import email_temp

emailTemplate = email_temp()

view = Blueprint("view",__name__,template_folder = "templates")

@view.route("/profile")
#home page with login and singin buttons and some additional info
def profile():
    if "email" in session:
        if request.method != 'GET':
            return redirect(url_for('event.page_404'))
        return render_template('profile.html')
    else:
        flash("you must login first")
        return redirect(url_for("public.login"))

@view.route("/api_command")
def api_command():
    if "email" in session:
        return render_template('api_command.html')
    else:
        flash("you must login first")
        return redirect(url_for("public.login"))

@view.route("/api_link")
def api_link():
    if "email" in session:
        return render_template('api_link.html')
    else:
        flash("you must login first")
        return redirect(url_for("public.login"))


@view.route("/fishing")
def fishing():
    if "email" in session:
        return render_template('api_link.html')
    else:
        flash("you must login first")
        return redirect(url_for("public.login"))


@view.route("/hooking")
def hooking():
    if "email" in session:
        return render_template('api_link.html')
    else:
        flash("you must login first")
        return redirect(url_for("public.login"))


@view.route("/code")
def code():
    if "email" in session:
        return render_template('api_link.html')
    else:
        flash("you must login first")
        return redirect(url_for("public.login"))
