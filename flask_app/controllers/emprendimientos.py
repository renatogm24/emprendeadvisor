from crypt import methods
from flask import jsonify,render_template,send_file, request
from flask_app import app
from flask_app.models import emprendimiento
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
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
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

    return result["translatedText"]

def getDataInstagrapi(igusername):
  cached = redis_server.get(igusername)
  if cached:
      parsed_json = (json.loads(cached))
      print("Serve from cached Emprendimiento Data")
  else:
      result = requests.get("https://salty-citadel-44293.herokuapp.com/"+igusername)
      data = result.text
      parsed_json = (json.loads(data))
      print(parsed_json["category_name"])
      parsed_json["category_name"] = translate_text("es",parsed_json["category_name"])
      data = json.dumps(parsed_json)
      redis_server.set(igusername, data)
      print("Serve from API Emprendimiento Data")
  return parsed_json

@app.route('/search',methods = ["POST"])
def search():
  igusername = request.form["search"]
  emprendimientoSearch = emprendimiento.Emprendimiento.search_by_username({"username":igusername})
  if not emprendimientoSearch: 
    result = getDataInstagrapi(igusername)
    if "error" in result:
      return render_template("emprendimiento.html",error=True)
    emprendAux = emprendimiento.Emprendimiento(result)
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