from flask import render_template, redirect, session,jsonify
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
  emprendimiento = {"category_id": ""}
  return render_template("emprendimiento.html",userSession=userSession, emprendimiento=emprendimiento)

@app.route('/cuenta')
def cuenta():
  userSession = ""
  if 'user_id' not in session:
    return redirect("/")
  if session["level"] == 9:
    return redirect("/admin")
  userSession = user.User.get_user_by_id({"id":session["user_id"]})
  return render_template("cuenta.html",userSession=userSession)

@app.route('/politica')
def politica():
  print("test")
  return render_template("politica.html")

@app.errorhandler(414)
def resource_max_sized(e):
    return jsonify(error="El archivo debe pesar menos de 5MB"), 414