from flask import render_template, request, redirect, flash, session, jsonify, url_for
from flask_app.models import user, category
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/admin')
def admin():
  if 'user_id' in session and session["level"] != 9:
    return redirect("/cuenta")
  if 'user_id' not in session:
    return redirect("/")
  categoriesList = category.Category.list_all_categories_with_subcategories()
  userSession = user.User.get_user_by_id({"id":session["user_id"]})
  return render_template("admin.html",userSession=userSession,categoriesList=categoriesList)


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

@app.route('/admin/users/block/<int:id>')
def blockUser(id):
    if 'level' in session and session["level"] != 9:
      return redirect("/")
    
    user_blocked = user.User.get_user_by_id({"id":id})
    if user_blocked.is_active == 1:
      blocked = 0
    else:
      blocked = 1
    user.User.update_state_blocked({"id":id,"blocked":blocked})
    response = {
      "users" : 1, 
    }
    return jsonify(response)



@app.route('/admin/categories/<int:id>')
def getCategory(id):
  if 'level' in session and session["level"] != 9:
    return redirect("/")
  categoryResult = category.Category.get_category({"id":id})
  if categoryResult != False:
    categoryResult = categoryResult.get_info_raw()
  response = {
      "categories" : categoryResult, 
    }
  return jsonify(response)


@app.route('/admin/categories/<string:is_active>/<int:limit>/<int:offset>')
def getCategories(is_active,limit,offset):
  if 'level' in session and session["level"] != 9:
    return redirect("/")
  if is_active not in ["active","requested"]:
    return redirect("/")
  if is_active == "active":
    is_active = 1
  else:
    is_active = 0

  categories = category.Category.list_categories({"level":1, "category_id":"" ,"limit":limit, "offset": offset, "is_active": is_active})
  endList = False

  if categories == False:
    response = {
      "categories" : [], 
      "endList" : True
    }
    return jsonify(response)

  if len(categories) < limit:
    endList = True
  response = {
      "categories" : list(map(lambda x : x.get_info_raw(), categories)), 
      "endList" : endList
    }
  return jsonify(response)


@app.route('/admin/searchCategories/<string:is_active>/<string:word>/<int:limit>/<int:offset>')
def searchCategories(is_active,word,limit,offset):
  if 'level' in session and session["level"] != 9:
    return redirect("/")
  
  if is_active not in ["active","requested"]:
    return redirect("/")
  if is_active == "active":
    is_active = 1
  else:
    is_active = 0

  likeWord = "%%"+word+"%%"
  categories = category.Category.get_categories_like({"level":1, "category_id":"", "limit":limit, "offset": offset, "word" : likeWord, "is_active": is_active})
  endList = False
  
  if categories == False:
    response = {
      "categories" : [], 
      "endList" : True
    }
    return jsonify(response)

  
  if len(categories) < limit:
    endList = True
  response = {
      "categories" : list(map(lambda x : x.get_info_raw(), categories)), 
      "endList" : endList
    }
  return jsonify(response)


@app.route('/admin/categories/<string:is_active>/list/<int:id>/<int:limit>/<int:offset>')
def getSubcategories(id,limit,offset,is_active):
  if 'level' in session and session["level"] != 9:
    return redirect("/")
  
  if is_active not in ["active","requested"]:
    return redirect("/")
  if is_active == "active":
    is_active = 1
  else:
    is_active = 0

  categories = category.Category.list_categories({"level":2, "category_id":id ,"limit":limit, "offset": offset, "is_active":is_active})
  endList = False

  if categories == False:
    response = {
      "categories" : [], 
      "endList" : True
    }
    return jsonify(response)

  if len(categories) < limit:
    endList = True
  response = {
      "categories" : list(map(lambda x : x.get_info_raw(), categories)), 
      "endList" : endList
    }
  return jsonify(response)


@app.route('/admin/categories/create', methods=['POST'])
def createCategories():
    if 'level' in session and session["level"] != 9:
      return redirect("/")

    categorie_validation = category.Category.validate_category(request.form)
    if not categorie_validation[0]:
      return jsonify(error = categorie_validation[1])
    
    data = {
      "name" : request.form["name"],
      "is_active" : "1"
    }    

    if request.form["category_id"] == "0":
      data["category_id"] = "0"
      data["level"] = 1
    else:
      data["category_id"] = request.form["category_id"]
      data["level"] = 2
    
    category_id = category.Category.save_category(data)
    if request.form["category_id"] == "0":
      data2 = {
      "name" : "General",
      "is_active" : "1",
      "level": "2",
      "category_id": category_id
    }  
      category.Category.save_category(data2)

    if category_id == False:
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

@app.route('/admin/categories/delete/<int:id>')
def deleteCategory(id):
    if 'level' in session and session["level"] != 9:
      return redirect("/")
    category.Category.delete_subcategories({"id":id})
    category_deleted = category.Category.delete_category({"id":id})
    response = {
      "categories" : category_deleted, 
    }
    return jsonify(response)

@app.route('/admin/categories/update', methods=['POST'])
def updateCategory():
    if 'level' in session and session["level"] != 9:
      return redirect("/")

    category_validation = category.Category.validate_category(request.form)
    if not category_validation[0]:
      return jsonify(error = category_validation[1])
    
    data = {
      "id" : request.form["id"],
      "name" : request.form["name"],
      "category_id" : request.form["category_id"],
    }    
    
    category.Category.updateCategoryAll(data)

    response = {
      "updated" : True, 
      "created" : False
    }
    return jsonify(response)

@app.route('/admin/categories/approve/<int:id>')
def approveCategory(id):
    if 'level' in session and session["level"] != 9:
      return redirect("/")

    category.Category.approveCategory({"id":id})

    response = {
      "categories" : 1, 
    }
    return jsonify(response)