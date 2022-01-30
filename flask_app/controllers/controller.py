from flask import render_template, redirect, session
from flask_app import app
from flask_app.models import user

@app.route('/')
def index():
  userSession = ""
  if 'user_id' in session:
    userSession = user.User.get_user_by_id({"id":session["user_id"]})
  return render_template("index.html",userSession=userSession)

@app.route('/emprendimiento')
def emprendimiento():
  userSession = ""
  if 'user_id' in session:
    userSession = user.User.get_user_by_id({"id":session["user_id"]})
  return render_template("emprendimiento.html",userSession=userSession)