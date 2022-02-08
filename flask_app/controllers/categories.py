from flask import render_template, request, redirect, flash, session, jsonify, url_for
from flask_app.models import user, category
from flask_app import app
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