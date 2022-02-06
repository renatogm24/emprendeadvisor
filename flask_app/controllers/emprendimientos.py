from flask import jsonify,render_template,send_file
from flask_app import app
from flask_app.models import emprendimiento
import requests
import json
import redis
from io import BytesIO
from instagrapi import Client

redis_server = redis.StrictRedis(host='localhost', port=6379)

cl = Client()
cl.login("renato.gm24", "Lc0de#2021")

def getIgData(igusername):
  url = "https://www.instagram.com/"+ igusername +"/channel/?__a=1"
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

def getDataInstagrapi(igusername):
  result = cl.user_info_by_username(igusername).dict()
  return result

@app.route('/search/<string:igusername>')
def search(igusername):
  emprendimientoSearch = emprendimiento.Emprendimiento.search_by_username({"username":igusername})
  if not emprendimientoSearch:
    emprendAux = emprendimiento.Emprendimiento(getDataInstagrapi(igusername))    
  return render_template("emprendimiento.html",emprendimiento=emprendAux)

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