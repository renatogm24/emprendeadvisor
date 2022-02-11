from flask_mail import Mail, Message
from flask_app import app
from flask import jsonify, render_template, request
from flask_app.models import user
import uuid
import redis
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

PASSWORD_REGEX = re.compile(r"^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$.])[\w\d@#$.]{6,12}$")
PASSWORD_REGEX_v2 = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,12}$")

mail = Mail(app)
redis_server = redis.StrictRedis(host='localhost', port=6379)

@app.route('/reset/resetpassword', methods=["POST"])
def resetpassword():
  if not PASSWORD_REGEX_v2.match(request.form["password"]):
    return jsonify(error="La contraseña debe tener mayusculas minuscilas 1 numero y 1 caracter especial y tener entre 6 a 12 caracteres")
  if request.form["password"] != request.form["password_repeat"]:
    return jsonify(error="No coinciden las contraseñas")
  
  email = redis_server.get(request.form["key"])
  pw_hash = bcrypt.generate_password_hash(request.form['password'])
  user.User.updatePasswordbyemail({"email":email,"password":pw_hash})
  return jsonify(updated=True)

@app.route('/reset/passwordreset/<string:key>')
def sendMail(key):
  return render_template('resetForm.html',key=key)

@app.route('/forgotpassword', methods = ["POST"])
def forgotpassword():
  data = { "email" : request.form["email"] }
  user_in_db = user.User.get_user_by_email(data)
  if not user_in_db:
    return jsonify(error="Invalid Email/Password")
  key = str(uuid.uuid4())  
  redis_server.setex(key, (60*20),request.form["email"])
  msg = Message(subject="Resetea tu clave",sender= app.config.get("MAIL_USERNAME"),recipients=[request.form["email"]])
  msg.html = render_template('resetPassword.html',key=key)
  mail.send(msg)
  return jsonify(send=True)