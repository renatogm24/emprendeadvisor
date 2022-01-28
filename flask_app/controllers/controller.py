from flask import render_template, redirect, session
from flask_app import app

@app.route('/')
def index():
  if 'user_id' in session:
    return redirect("/dashboard")
  return render_template("index.html")