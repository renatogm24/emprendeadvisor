from flask import render_template, request, redirect, flash, session, jsonify, url_for
from flask_app.controllers.controller import emprendimiento
from flask_app.models import user, category, emprendimiento as empModel
from flask_app import app
from flask_app.controllers.emprendimientos import getDataInstagrapi
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/categories')
def getAllCategories():
  categories = category.Category.list_all_categories()
  if not categories:
    return jsonify({"categories":[]})
  response = {
      "categories" : list(map(lambda x : x.get_info_raw(), categories)), 
    }
  return jsonify(response)

@app.route('/subcategories/<int:id>')
def getSubcategoriesUser(id):
  categories = category.Category.list_subcategories({"id":id})
  if not categories:
    return jsonify({"categories":[]})
  response = {
      "categories" : list(map(lambda x : x.get_info_raw(), categories)), 
    }
  return jsonify(response)

@app.route('/categories/create', methods=['POST'])
def userCreateCategory():
    igname = request.form["pathname"].split("/")[-1]
    dataIG = getDataInstagrapi(igname)

    if "categoria" in request.form and "subcategoria" in request.form and "haveCategory" not in request.form and "haveSubcategory" not in request.form:
      #No se añade ningun categoria, se agrega el negocio y se asigna a la categoria asociada
      dataIG["category_id"] = request.form["subcategoria"]
      empModel.Emprendimiento.save(dataIG)
      response = {
        "redirect" : True,
        "url" : request.form["pathname"]
      }
      return jsonify(response)
    elif "haveCategory" in request.form and "haveSubcategory" not in request.form:
      #Se añade general
      data = {
        "name": request.form["nuevaCategoria"],
        "is_active":0,
        "level": 1,
        "category_id":"0"
      }
      categorie_validation = category.Category.validate_category(data)
      if not categorie_validation[0]:
        return jsonify(error = categorie_validation[1])
      id = category.Category.save_category(data)
      data2 = {
        "name": "General",
        "is_active":0,
        "level": 2,
        "category_id": id
      }
      categorie_validation2 = category.Category.validate_category(data2)
      if not categorie_validation2[0]:
        return jsonify(error = categorie_validation2[1])
      newId = category.Category.save_category(data2)
      dataIG["category_id"] = newId
      empModel.Emprendimiento.save(dataIG)

    elif "haveSubcategory" in request.form and "haveCategory" in request.form:
      data = {
        "name": request.form["nuevaCategoria"],
        "is_active":0,
        "level": 1,
        "category_id":"0"
      }

      categorie_validation = category.Category.validate_category(data)
      if categorie_validation[0]:
        id = category.Category.save_category(data)
        data2 = {
        "name": "General",
        "is_active":0,
        "level": 2,
        "category_id": id
        }
        category.Category.save_category(data2)
      else:
        id = category.Category.get_category_by_name({"name": request.form["nuevaCategoria"] }).id
        
      data3 = {
        "name": request.form["nuevaSubcategoria"],
        "is_active":0,
        "level": 2,
        "category_id": id
      }
      categorie_validation3 = category.Category.validate_category(data3)
      if not categorie_validation3[0]:
        return jsonify(error = categorie_validation3[1])
      newId2 = category.Category.save_category(data3)
      dataIG["category_id"] = newId2
      empModel.Emprendimiento.save(dataIG)

    response = {
      "created" : True, 
    }
    return jsonify(response)