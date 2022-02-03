from flask import render_template, request, redirect, flash, session, jsonify, url_for
from flask_app.models import user
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask.sessions import SecureCookieSessionInterface

session_cookie = SecureCookieSessionInterface().get_signing_serializer(app)

@app.route('/register/user', methods=['POST'])
def register():
    user_validation = user.User.validate_user(request.form)
    if not user_validation[0]:
      return jsonify(error = user_validation[1])
    # validar el formulario aquí...
    # crear el hash
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    
    # poner pw_hash en el diccionario de datos
    data = {
      "first_name": request.form['first_name'],
      "last_name": request.form['last_name'],
      "email": request.form['email'],
      "password" : pw_hash
    }
    # llama al @classmethod de guardado en Usuario
    user_id = user.User.save(data)
    # almacenar id de usuario en la sesión
    session['user_id'] = user_id
    response = {
      "redirectUrl" : request.form["pathname"], 
      "isRedirect" : True 
    }
    return jsonify(response)

@app.after_request
@app.route('/login', methods=['POST'])
def login():
    # ver si el nombre de usuario proporcionado existe en la base de datos
    data = { "email" : request.form["email"] }
    user_in_db = user.User.get_user_by_email(data)
    # usuario no está registrado en la base de datos
    if not user_in_db:
      return jsonify(error="Invalid Email/Password")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
      return jsonify(error="Invalid Email/Password")
    session['user_id'] = user_in_db.id
    response = {
      "redirectUrl" : request.form["pathname"], 
      "isRedirect" : True 
    }
    same_cookie = session_cookie.dumps(dict(session))
    toreturn = jsonify(response).headers.add("Set-Cookie", f"my_cookie={same_cookie}; Secure; HttpOnly; SameSite=None; Path=/;")
    return toreturn

@app.route('/dashboard')
def dashboard():
  userSession = ""
  if 'user_id' in session:
    userSession = user.User.get_user_by_id({"id":session["user_id"]})
  return render_template("dashboard.html",userSession=userSession)


@app.route('/getUserSession')
def getUserSession():
  userSession = ""
  if 'user_id' not in session:
    return redirect("/")
  userSession = user.User.get_user_by_id({"id":session["user_id"]})
  return userSession.get_info()

@app.route('/updateProfile', methods=['POST'])
def updateProfile():
    data = {
      "id" : session["user_id"],
      "first_name" : request.form["first_name"],
      "last_name" : request.form["last_name"],
      "email" : request.form["email"]
    }
    user_validation = user.User.validate_update(data)
    if not user_validation[0]:
      return jsonify(error = user_validation[1])
    
    user.User.updateUser(data)

    response = {
      "updated" : True, 
    }
    return jsonify(response)

@app.route('/updatePassword', methods=['POST'])
def updatePassword():
    user_validation = user.User.validate_password(request.form)
    if not user_validation[0]:
      return jsonify(error = user_validation[1])
    
    user_in_db = user.User.get_user_by_id({"id": session["user_id"]})
    if not bcrypt.check_password_hash(user_in_db.password, request.form['actual_password']):
      return jsonify(error="Incorrect password")
    
    data = {
      "id" : session["user_id"],
      "password" : bcrypt.generate_password_hash(request.form['password']),
    }
    user.User.updatePassword(data)

    response = {
      "updated" : True, 
    }
    return jsonify(response)


@app.route('/logout')
def logout():
  session.clear()
  return redirect("/")
