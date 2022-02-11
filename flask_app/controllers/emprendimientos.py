from flask import jsonify,render_template,send_file, request, session, redirect
from flask_app import app
from flask_app.models import emprendimiento, user,category, review, image as upload
import requests
import json
import redis
from io import BytesIO
from werkzeug.utils import secure_filename
from flask_app.controllers.users import upload_file_to_s3

redis_server = redis.StrictRedis(host='localhost', port=6379)

def getIgData(igusername):
  url = "https://www.instagram.com/"+ igusername +"/?__a=1"
  r  = requests.get(url)
  data = r.text
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
        parsed_json = (json.loads(data))
        parsed_json["category_name"] = translate_text("es",parsed_json["category_name"])
        data = json.dumps(parsed_json)
        redis_server.set(igusername, data)
        print("Serve from API Emprendimiento Data")
      except:
        parsed_json = {"error":True}
  return parsed_json
  
@app.route('/search/')
def searchEmpty():
  return redirect("/dashboard")

@app.route('/search/<string:igusername>')
def search(igusername):
  igusername = igusername.lower()
  igusername = igusername.replace("@","")
  if igusername == "":
    return redirect("/dashboard")
  emprendimientoSearch = emprendimiento.Emprendimiento.search_by_username({"username":igusername})
  if not emprendimientoSearch: 
    result = getDataInstagrapi(igusername)
    if "error" in result:
      return render_template("emprendimiento.html",error=True)
    emprendAux = emprendimiento.Emprendimiento(result)
  else:
    return redirect("/emprendimiento/"+str(emprendimientoSearch["id"]))
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
  user_session_id = "0"
  if 'user_id' in session:
    userSession = user.User.get_user_by_id({"id":session["user_id"]})
    user_session_id = userSession.id
  categoriesList = category.Category.list_all_categories_with_subcategories()
  reviewsList = review.Review.list_reviews_by_id({"id":id,"offset":0,"limit":3,"user_session_id":user_session_id})
  opiniones = review.Review.get_opiniones({"id":id})
  return render_template("emprendimiento.html",emprendimiento=emprendAux,userSession=userSession,categoriesList=categoriesList, reviewsList=reviewsList,opiniones=opiniones)

@app.route('/comentarios/loadmore', methods = ["POST"])
def loadmorecomments():
  offset = request.form["offset"]
  id = request.form["review_id"]
  limit = 3
  offset = int(offset)
  rating = request.form["rating"]
  user_session_id = "0"
  if 'user_id' in session:
    userSession = user.User.get_user_by_id({"id":session["user_id"]})
    user_session_id = userSession.id
  reviewsList = review.Review.list_reviews_by_id({"id":id,"offset":offset,"limit":limit,"user_session_id":user_session_id,"rating":rating})
  endList = False
  
  if reviewsList == False:
    response = {
      "reviews" : [], 
      "endList" : True
    }
    return jsonify(response)
  
  if len(reviewsList) < limit:
    endList = True
  response = {
      "reviews" : list(map(lambda x : x.get_info_raw_w_user(), reviewsList)), 
      "endList" : endList
    }
  return jsonify(response)


@app.route('/comentarios/crear', methods = ["POST"])
def createcomment():
  review_validation = review.Review.validate(request.form)
  if not review_validation[0]:
    return jsonify(error = review_validation[1])
  
  data = {
    "rating": request.form["rating"],
    "title": request.form["title"].replace("%", " por ciento"),
    "departamento": request.form["departamento"],
    "provincia": request.form["provincia"],
    "distrito": request.form["distrito"],
    "comment": request.form["comment"].replace("%", " por ciento"),
    "emprendimiento_id": request.form["emprendimiento_id"],
    "user_id":session["user_id"]
  }
  
  newId = review.Review.save(data)

  files = request.files.getlist("images")
  for file in files:
    url = ""
    if file.filename != "":
        if file:
            file.filename = secure_filename(file.filename)
            fileType = file.content_type
            arrTypes = fileType.split("/")
            if arrTypes[0] != "image" or arrTypes[1] not in ["jpeg","jpg","png"]:
              return jsonify(error = f"Formatos permitidos: jpg, jpeg, png")
            url = upload_file_to_s3(file, app.config["S3_BUCKET"])
            upload.Image.save_review_image({"url":url,"review_id":newId})

  response = {
      "created" : True
    }
  return jsonify(response)

@app.route('/comentarios/report', methods = ["POST"])
def createreport():
  if len(request.form["text"])<1:
    return jsonify(error = "Texto vacio")
  
  data = {
    "text": request.form["text"],
    "review_id": request.form["review_id"],
    "user_id":session["user_id"]
  }
  
  review.Review.createReport(data)

  response = {
      "created" : True
    }
  return jsonify(response)

@app.route('/emprendimientos/category/<int:id>')
def getCategoriesEmp(id):
  userSession = ""
  if 'user_id' in session:
    userSession = user.User.get_user_by_id({"id":session["user_id"]})
  categoriesList = category.Category.list_all_categories_with_subcategories()
  dataMaxMin = emprendimiento.Emprendimiento.get_emprendimientos_max_min({"category_id":id})
  if dataMaxMin["max_promedio"] == None:
    dataMaxMin = {'max_promedio': 0, 'min_promedio': 0, 'max_reviews': 0, 'min_reviews': 0, 'max_followers': 0, 'min_followers': 0}
  emprendimientoList = emprendimiento.Emprendimiento.get_emprendimientos({
    "offset":0,"limit":8,"order_by":"promedio","category_id":id,
    'max_promedio': dataMaxMin["max_promedio"], 
    'min_promedio': dataMaxMin["min_promedio"], 
    'max_reviews': dataMaxMin["max_reviews"], 
    'min_reviews': dataMaxMin["min_reviews"], 
    'max_followers': dataMaxMin["max_followers"], 
    'min_followers': dataMaxMin["min_followers"]
    })
 
  totalCuenta = emprendimiento.Emprendimiento.get_emprendimientos_total_count({"category_id":id})
  categoryObj = category.Category.get_category_by_id({"id":id})
  tipo = "categoria"
  categoria = categoryObj.name
  pathCategory = id
  return render_template("dashboard.html",userSession=userSession,categoriesList=categoriesList,emprendimientoList=emprendimientoList,dataMaxMin=dataMaxMin,totalCuenta=totalCuenta,tipo=tipo,categoria=categoria,pathCategory=pathCategory)


@app.route('/emprendimientos/subcategory/<int:id>')
def getSubcategoriesEmp(id):
  userSession = ""
  if 'user_id' in session:
    userSession = user.User.get_user_by_id({"id":session["user_id"]})
  categoriesList = category.Category.list_all_categories_with_subcategories()
  dataMaxMin = emprendimiento.Emprendimiento.get_emprendimientos_max_min({"category_id":id})
  if dataMaxMin["max_promedio"] == None:
    dataMaxMin = {'max_promedio': 0, 'min_promedio': 0, 'max_reviews': 0, 'min_reviews': 0, 'max_followers': 0, 'min_followers': 0}
  
  emprendimientoList = emprendimiento.Emprendimiento.get_emprendimientos({
    "offset":0,"limit":8,"order_by":"promedio","category_id":id,
    'max_promedio': dataMaxMin["max_promedio"], 
    'min_promedio': dataMaxMin["min_promedio"], 
    'max_reviews': dataMaxMin["max_reviews"], 
    'min_reviews': dataMaxMin["min_reviews"], 
    'max_followers': dataMaxMin["max_followers"], 
    'min_followers': dataMaxMin["min_followers"]
    })
  
  totalCuenta = emprendimiento.Emprendimiento.get_emprendimientos_total_count({"category_id":id})
  categoryObj = category.Category.get_category_by_id({"id":id})
  tipo = "subcategoria"
  categoria = categoryObj.name
  subcategoria = categoryObj.padre
  pathCategory = id
  return render_template("dashboard.html",userSession=userSession,categoriesList=categoriesList,emprendimientoList=emprendimientoList,dataMaxMin=dataMaxMin,totalCuenta=totalCuenta,tipo=tipo,subcategoria=subcategoria,categoria=categoria,pathCategory=pathCategory)

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

  if "category_id" in request.form:
    data["category_id"] = request.form["category_id"]
  
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