from flask import render_template, request, redirect, flash, session, jsonify, url_for
from flask_app.models import user
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/admin')
def admin():
  userSession = ""
  if 'user_id' not in session:
    return redirect("/")
  userSession = user.User.get_user_by_id({"id":session["user_id"]})
  return render_template("admin.html",userSession=userSession)


@app.route('/admin/users/<int:id>')
def getUser(id):
  # Falta validar si es admin
  if 'user_id' not in session:
    return redirect("/")
  userResult = user.User.get_user_by_id({"id":id})
  if userResult != False:
    userResult = userResult.get_info_raw_complete()
  response = {
      "user" : userResult, 
    }
  return jsonify(response)


@app.route('/admin/users/<int:limit>/<int:offset>')
def getUsers(limit,offset):
  # Falta validar si es admin
  if 'user_id' not in session:
    return redirect("/")
  users = user.User.get_users_except_admin({"id":session["user_id"],"limit":limit, "offset": offset})
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


@app.route('/admin/searchUsers/<string:word>/<int:limit>/<int:offset>')
def searchUsers(word,limit,offset):
  # Falta validar si es admin
  if 'user_id' not in session:
    return redirect("/")
  likeWord = "%%"+word+"%%"
  users = user.User.get_users_except_admin_like({"id":session["user_id"],"limit":limit, "offset": offset, "word" : likeWord})
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
    }
    return jsonify(response)

@app.route('/admin/users/delete/<int:id>')
def deleteUser(id):
    user_deleted = user.User.delete({"id":id})
    response = {
      "user" : user_deleted, 
    }
    return jsonify(response)
