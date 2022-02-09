from flask import jsonify,render_template,send_file, request, session
from flask_app import app
from flask_app.models import emprendimiento, user,category
import requests
import json
import redis
from io import BytesIO

redis_server = redis.StrictRedis(host='localhost', port=6379)

def getIgData(igusername):
  url = "https://www.instagram.com/"+ igusername +"/?__a=1"
  print(url)
  r  = requests.get(url)
  #r.encoding = "ascii"
  data = r.text
  print(data)
  parsed_json = (json.loads(data))

  username = parsed_json["graphql"]["user"]["username"]
  full_name = parsed_json["graphql"]["user"]["full_name"]
  fbid = parsed_json["graphql"]["user"]["fbid"]
  biography = parsed_json["graphql"]["user"]["biography"]
  external_url = parsed_json["graphql"]["user"]["external_url"]
  edge_followed_by = parsed_json["graphql"]["user"]["edge_followed_by"]["count"]
  is_business_account = parsed_json["graphql"]["user"]["is_business_account"]
  business_address_json = parsed_json["graphql"]["user"]["business_address_json"]
  business_email = parsed_json["graphql"]["user"]["business_email"]
  business_phone_number = parsed_json["graphql"]["user"]["business_phone_number"]
  category_name = parsed_json["graphql"]["user"]["category_name"]
  is_private = parsed_json["graphql"]["user"]["is_private"]
  profile_pic_url = parsed_json["graphql"]["user"]["profile_pic_url"]
  profile_pic_url_hd = parsed_json["graphql"]["user"]["profile_pic_url_hd"].split("?")
  images_nodes = parsed_json["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][:4]
  images = list(map(lambda x : x["node"]["thumbnail_src"], images_nodes))

  response = {
      "username" : username,
      "full_name" : full_name,
      "fbid" : fbid,
      "biography": biography,
      "external_url" : external_url, 
      "edge_followed_by" : edge_followed_by,
      "is_business_account": is_business_account,
      "business_address_json": business_address_json,
      "business_email": business_email,
      "business_phone_number": business_phone_number,
      "category_name" : category_name,
      "is_private": is_private,
      "profile_pic_url" :profile_pic_url,
      "profile_pic_url_hd": profile_pic_url_hd,
      "images" : images
    }

  return response

def translate_text(target, text):
    try:
      import os
      os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/ubuntu/emprendeadvisor-e0425dce8ff1.json"
      import six
      from google.cloud import translate_v2 as translate

      translate_client = translate.Client()

      if isinstance(text, six.binary_type):
          text = text.decode("utf-8")

      # Text can also be a sequence of strings, in which case this method
      # will return a sequence of results for each text.
      result = translate_client.translate(text, target_language=target)
      result = result["translatedText"]
    except:
      result = text
    return result

def getDataInstagrapi(igusername):
  cached = redis_server.get(igusername)
  if cached:
      parsed_json = (json.loads(cached))
      print("Serve from cached Emprendimiento Data")
  else:
      try:
        result = requests.get("https://salty-citadel-44293.herokuapp.com/"+igusername)
        data = result.text
        print(data)
        parsed_json = (json.loads(data))
        parsed_json["category_name"] = translate_text("es",parsed_json["category_name"])
        data = json.dumps(parsed_json)
        redis_server.set(igusername, data)
        print("Serve from API Emprendimiento Data")
      except:
        parsed_json = {"error":True}
  return parsed_json

@app.route('/search/<string:igusername>')
def search(igusername):
  igusername = igusername.lower()
  emprendimientoSearch = emprendimiento.Emprendimiento.search_by_username({"username":igusername})
  if not emprendimientoSearch: 
    result = getDataInstagrapi(igusername)
    if "error" in result:
      return render_template("emprendimiento.html",error=True)
    emprendAux = emprendimiento.Emprendimiento(result)
  else:
    emprendAux = emprendimiento.Emprendimiento(emprendimientoSearch)
    categoryEmp = category.Category.get_category_by_id({"id":emprendAux.category_id})
    emprendAux.categoria = categoryEmp.name
    emprendAux.subcategoria = categoryEmp.padre
  userSession = ""
  if 'user_id' in session:
    userSession = user.User.get_user_by_id({"id":session["user_id"]})
  categoriesList = category.Category.list_all_categories_with_subcategories()

  return render_template("emprendimiento.html",emprendimiento=emprendAux,userSession=userSession,categoriesList=categoriesList)

@app.route('/emprendimiento/<int:id>')
def getById(id):
  emprendimientoSearch = emprendimiento.Emprendimiento.search_by_id({"id":id})
  if not emprendimientoSearch: 
    return render_template("emprendimiento.html",error=True)
  else:
    emprendAux = emprendimiento.Emprendimiento(emprendimientoSearch)
    categoryEmp = category.Category.get_category_by_id({"id":emprendAux.category_id})
    emprendAux.categoria = categoryEmp.name
    emprendAux.subcategoria = categoryEmp.padre

  userSession = ""
  if 'user_id' in session:
    userSession = user.User.get_user_by_id({"id":session["user_id"]})
  categoriesList = category.Category.list_all_categories_with_subcategories()
  return render_template("emprendimiento.html",emprendimiento=emprendAux,userSession=userSession,categoriesList=categoriesList)

@app.route('/emprendimientos/category/<int:id>')
def getCategoriesEmp(id):
  userSession = ""
  if 'user_id' in session:
    userSession = user.User.get_user_by_id({"id":session["user_id"]})
  categoriesList = category.Category.list_all_categories_with_subcategories()
  emprendimientoList = emprendimiento.Emprendimiento.get_emprendimientos({"offset":0,"limit":8,"order_by":"promedio","category_id":id})
  dataMaxMin = emprendimiento.Emprendimiento.get_emprendimientos_max_min({"category_id":id})
  if dataMaxMin["max_promedio"] == None:
    dataMaxMin = {'max_promedio': 0, 'min_promedio': 0, 'max_reviews': 0, 'min_reviews': 0, 'max_followers': 0, 'min_followers': 0}
  totalCuenta = emprendimiento.Emprendimiento.get_emprendimientos_total_count({"category_id":id})
  categoryObj = category.Category.get_category_by_id({"id":id})
  tipo = "categoria"
  categoria = categoryObj.name
  return render_template("dashboard.html",userSession=userSession,categoriesList=categoriesList,emprendimientoList=emprendimientoList,dataMaxMin=dataMaxMin,totalCuenta=totalCuenta,tipo=tipo,categoria=categoria)


@app.route('/emprendimientos/subcategory/<int:id>')
def getSubcategoriesEmp(id):
  userSession = ""
  if 'user_id' in session:
    userSession = user.User.get_user_by_id({"id":session["user_id"]})
  categoriesList = category.Category.list_all_categories_with_subcategories()
  emprendimientoList = emprendimiento.Emprendimiento.get_emprendimientos({"offset":0,"limit":8,"order_by":"promedio","category_id":id})
  dataMaxMin = emprendimiento.Emprendimiento.get_emprendimientos_max_min({"category_id":id})
  if dataMaxMin["max_promedio"] == None:
    dataMaxMin = {'max_promedio': 0, 'min_promedio': 0, 'max_reviews': 0, 'min_reviews': 0, 'max_followers': 0, 'min_followers': 0}
  totalCuenta = emprendimiento.Emprendimiento.get_emprendimientos_total_count({"category_id":id})
  categoryObj = category.Category.get_category_by_id({"id":id})
  tipo = "subcategoria"
  categoria = categoryObj.name
  subcategoria = categoryObj.padre
  return render_template("dashboard.html",userSession=userSession,categoriesList=categoriesList,emprendimientoList=emprendimientoList,dataMaxMin=dataMaxMin,totalCuenta=totalCuenta,tipo=tipo,subcategoria=subcategoria,categoria=categoria)

@app.route('/img/<path:url>&<params>')
def image(url,params):
    image_url = "{}?{}".format(url, params)    
    cached = redis_server.get(image_url)
    if cached:
        buffer_image = BytesIO(cached)
        buffer_image.seek(0)
        print("Get from cached")
    else:
        r = requests.get(image_url)  # you can add UA, referrer, here is an example.
        buffer_image = BytesIO(r.content)
        buffer_image.seek(0)
        redis_server.setex(image_url, (60*60*24*7),buffer_image.getvalue())
        print("Get from API")
    return send_file(buffer_image, mimetype='image/jpeg')

@app.route('/emprendimientos/loadmore', methods = ["POST"])
def loadmore():
  limit = 8

  data = {
    "offset" : int(request.form["offset"]),
    "limit" : limit,
    "order_by" : request.form["order_by"],
    "min_promedio" : float(request.form["min_promedio"]),
    "max_promedio" : float(request.form["max_promedio"]),
    "min_reviews" : int(request.form["min_reviews"]),
    "max_reviews" : int(request.form["max_reviews"]),
    "min_followers" : int(request.form["min_followers"]),
    "max_followers" : int(request.form["max_followers"])
  }
  
  emprendimientoList = emprendimiento.Emprendimiento.get_emprendimientos(data)
  endList = False
  
  if emprendimientoList == False:
    response = {
      "emprendimientos" : [], 
      "endList" : True
    }
    return jsonify(response)

  if len(emprendimientoList) < limit:
    endList = True
  response = {
      "emprendimientos" : list(map(lambda x : x.get_info_raw(), emprendimientoList)), 
      "endList" : endList
    }
  return jsonify(response)