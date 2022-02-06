from flask import render_template, request, redirect, flash, session, jsonify, url_for
from flask_app.models import user, image
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
import boto3, botocore
from werkzeug.utils import secure_filename
import uuid
import json
import os

s3 = boto3.client(
   "s3",
   aws_access_key_id=app.config['S3_KEY'],
   aws_secret_access_key=app.config['S3_SECRET']
)

def upload_file_to_s3(file, bucket_name, acl="public-read"):
    """
    Docs: http://boto3.readthedocs.io/en/latest/guide/s3.html
    """
    arrFilString = file.content_type.split("/")
    file_name_uuid = str(uuid.uuid4()) + "." + arrFilString[-1]
    try:
        s3.upload_fileobj(
            file,
            bucket_name,
            file_name_uuid,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type    #Set appropriate content type as per the file
            }
        )
    except Exception as e:
        print("Something Happened: ", e)
        return e
    return "{}{}".format(app.config["S3_LOCATION"], file_name_uuid)

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
    session['level'] = 1
    response = {
      "redirectUrl" : request.form["pathname"], 
      "isRedirect" : True 
    }
    return jsonify(response)

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
    if user_in_db.is_active == 0:
      return jsonify(error="Usuario bloqueado")
    session['user_id'] = user_in_db.id
    session['level'] = user_in_db.level
    response = {
      "redirectUrl" : request.form["pathname"], 
      "isRedirect" : True 
    }
    toreturn = jsonify(response)
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

    # Agregar imagen
    file = request.files["image"]
    url = ""
    if file.filename != "":
      if file:
          file.filename = secure_filename(file.filename)
          photo_size = request.files['image'].read()
          size = len(photo_size)/1024/1024 #file in mb
          if(size > 5):
            return jsonify(error = "La foto seleccionada pesa más de 5MB, elige una de menor tamaño")
          arrTypes = file.content_type.split("/")
          if arrTypes[0] != "images" or arrTypes[0] not in ["jpeg","jpg","png"]:
            return jsonify(error = "Formatos permitidos: jpg, jpeg, png")
          url = upload_file_to_s3(file, app.config["S3_BUCKET"])
          idImage = image.Image.save_profile_image({"url":url})      
          data["image_id"] = idImage
          user.User.updateUserWithImg(data)
          actualUrlDB = request.form["actualImage"]
          actualUrl = actualUrlDB.replace("http://emprendeadvisor.s3.amazonaws.com/","")
          response = s3.delete_object(Bucket='emprendeadvisor',Key=actualUrl)
          image.Image.delete_image_by_url({"url":actualUrlDB})

    else:
      user.User.updateUser(data)
    response = {
      "updated" : True, 
      "url": url
    }
    return jsonify(response)

@app.route('/deleteImageAndReset', methods=['POST'])
def deleteImageAndReset():
    url = request.form["json"]
    urlFormat = json.loads(url)
    urlString = urlFormat["url"]
    urlBucket = urlString.replace("http://emprendeadvisor.s3.amazonaws.com/","")
    s3.delete_object(Bucket='emprendeadvisor',Key=urlBucket)
    user.User.resetImgUser({"id": session["user_id"]})
    image.Image.delete_image_by_url({"url":urlString})
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
