from flask import render_template, request, redirect, flash, session, jsonify, url_for
from flask_app.models import user
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/admin')
def admin():
  if 'user_id' in session and session["level"] != 9:
    return redirect("/cuenta")
  if 'user_id' not in session:
    return redirect("/")
  userSession = user.User.get_user_by_id({"id":session["user_id"]})
  return render_template("admin.html",userSession=userSession)


@app.route('/admin/users/<int:id>')
def getUser(id):
  if 'level' in session and session["level"] != 9:
    return redirect("/")
  userResult = user.User.get_user_by_id({"id":id})
  if userResult != False:
    userResult = userResult.get_info_raw_complete()
  response = {
      "users" : userResult, 
    }
  return jsonify(response)


@app.route('/admin/users/<string:is_active>/<int:limit>/<int:offset>')
def getUsers(is_active,limit,offset):
  if 'level' in session and session["level"] != 9:
    return redirect("/")
  if is_active not in ["active","blocked"]:
    return redirect("/")
  if is_active == "active":
    is_active = 1
  else:
    is_active = 0

  users = user.User.get_users_except_admin({"id":session["user_id"],"limit":limit, "offset": offset, "is_active": is_active})
  endList = False

  if users == False:
    response = {
      "users" : [], 
      "endList" : True
    }
    return jsonify(response)

  if len(users) < limit:
    endList = True
  response = {
      "users" : list(map(lambda x : x.get_info_raw(), users)), 
      "endList" : endList
    }
  return jsonify(response)


@app.route('/admin/searchUsers/<string:is_active>/<string:word>/<int:limit>/<int:offset>')
def searchUsers(is_active,word,limit,offset):
  if 'level' in session and session["level"] != 9:
    return redirect("/")
  
  if is_active not in ["active","blocked"]:
    return redirect("/")
  if is_active == "active":
    is_active = 1
  else:
    is_active = 0

  likeWord = "%%"+word+"%%"
  users = user.User.get_users_except_admin_like({"id":session["user_id"],"limit":limit, "offset": offset, "word" : likeWord, "is_active": is_active})
  endList = False
  
  if users == False:
    response = {
      "users" : [], 
      "endList" : True
    }
    return jsonify(response)

  
  if len(users) < limit:
    endList = True
  response = {
      "users" : list(map(lambda x : x.get_info_raw(), users)), 
      "endList" : endList
    }
  return jsonify(response)

@app.route('/admin/users/update', methods=['POST'])
def updateUser():
    if 'level' in session and session["level"] != 9:
      return redirect("/")

    user_validation = user.User.validate_user_update(request.form)
    if not user_validation[0]:
      return jsonify(error = user_validation[1])

    passwordForm = request.form['password']
    if len(passwordForm)<13:
      passwordForm = bcrypt.generate_password_hash(request.form['password'])
    
    data = {
      "id" : request.form["id"],
      "first_name" : request.form["first_name"],
      "last_name" : request.form["last_name"],
      "email" : request.form["email"],
      "password": passwordForm
    }    
    
    user.User.updateUserAll(data)

    response = {
      "updated" : True, 
      "created" : False
    }
    return jsonify(response)

@app.route('/admin/users/create', methods=['POST'])
def createUser():
    if 'level' in session and session["level"] != 9:
      return redirect("/")

    user_validation = user.User.validate_user_admin(request.form)
    if not user_validation[0]:
      return jsonify(error = user_validation[1])
    
    data = {
      "id" : request.form["id"],
      "first_name" : request.form["first_name"],
      "last_name" : request.form["last_name"],
      "email" : request.form["email"],
      "password": bcrypt.generate_password_hash(request.form['password'])
    }    
    
    user_id = user.User.save(data)

    if user_id == False:
      response = {
      "updated" : False, 
      "created" : False
      }
      return jsonify(response)

    response = {
      "updated" : False, 
      "created" : True
    }
    return jsonify(response)

@app.route('/admin/users/delete/<int:id>')
def deleteUser(id):
    if 'level' in session and session["level"] != 9:
      return redirect("/")
    user_deleted = user.User.delete({"id":id})
    response = {
      "users" : user_deleted, 
    }
    return jsonify(response)
