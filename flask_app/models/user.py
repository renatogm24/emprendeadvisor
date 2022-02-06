from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, jsonify
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r"^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$.])[\w\d@#$.]{6,12}$")
PASSWORD_REGEX_UPDATE = re.compile(r"^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$.])[\w\d@#$.]{6,80}$")

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.is_active = data['is_active']
        self.level = data['level']
        self.image = ""
    
    def get_info(self):
      data = {
          'id': self.id,
          'first_name': self.first_name,
          'last_name': self.last_name,
          'email': self.email,
          'image': self.image
      }
      return jsonify(data)

    def get_info_raw(self):
      data = {
          'id': self.id,
          'first_name': self.first_name,
          'last_name': self.last_name,
          'email': self.email,
          'image': self.image
      }
      return data

    def get_info_raw_complete(self):
      data = {
          'id': self.id,
          'first_name': self.first_name,
          'last_name': self.last_name,
          'email': self.email,
          'password': self.password,
      }
      return data
    
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO users (first_name, last_name, email , password, created_at, updated_at, image_id, is_active, level ) VALUES ( %(first_name)s , %(last_name)s ,%(email)s ,%(password)s ,NOW() , NOW(), 1, 1, 1 );"
        return connectToMySQL('emprendeadvisor').query_db( query, data )

    @classmethod
    def delete(cls, data ):
        query = "DELETE FROM users where id = %(id)s;"
        return connectToMySQL('emprendeadvisor').query_db( query, data )

    @classmethod
    def updateUser(cls, data ):
        query = "UPDATE users SET first_name = %(first_name)s ,last_name = %(last_name)s,email = %(email)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL('emprendeadvisor').query_db( query, data )
    
    @classmethod
    def updateUserWithImg(cls, data ):
        query = "UPDATE users SET first_name = %(first_name)s ,last_name = %(last_name)s,email = %(email)s, image_id = %(image_id)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL('emprendeadvisor').query_db( query, data )

    @classmethod
    def resetImgUser(cls, data ):
        query = "UPDATE users SET image_id = 1 WHERE id = %(id)s;"
        return connectToMySQL('emprendeadvisor').query_db( query, data )

    @classmethod
    def update_state_blocked(cls, data ):
        query = "UPDATE users SET is_active = %(blocked)s , updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL('emprendeadvisor').query_db( query, data )

    @classmethod
    def updateUserAll(cls, data ):
        query = "UPDATE users SET first_name = %(first_name)s ,last_name = %(last_name)s,email = %(email)s, password= %(password)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL('emprendeadvisor').query_db( query, data )

    @classmethod
    def updatePassword(cls, data ):
        query = "UPDATE users SET password = %(password)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL('emprendeadvisor').query_db( query, data )

    @classmethod
    def get_user_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('emprendeadvisor').query_db(query,data)
        if len(results) < 1:
          return False
        return cls(results[0])

    @classmethod
    def get_user_by_id(cls,data):
        query = "SELECT * FROM users left join images on users.image_id = images.id WHERE users.id = %(id)s;"
        results = connectToMySQL('emprendeadvisor').query_db(query,data)
        if len(results) < 1:
          return False
        user = cls(results[0])
        user.image = results[0]["url"]
        return user

    @classmethod
    def get_users_except_id(cls,data):
        query = "SELECT * FROM users WHERE id != %(id)s is_active = %(is_active)s;"
        results = connectToMySQL('emprendeadvisor').query_db(query,data)
        users = []
        if len(results) < 1:
          return False
        for user in results:
          users.append(cls(user))
        return users

    @classmethod
    def exist_mail(cls,data):
        query = "SELECT * FROM users where email = %(email)s;"
        results = connectToMySQL('emprendeadvisor').query_db(query,data)
        if len(results) == 0:
          return False
        else:
          return True

    #Falta actualizar query que no tome usuarios admin
    @classmethod
    def get_users_except_admin(cls,data):
        query = "SELECT * FROM users WHERE id != %(id)s and level != 9 and is_active = %(is_active)s limit %(offset)s,%(limit)s;"
        results = connectToMySQL('emprendeadvisor').query_db(query,data)
        users = []
        if len(results) < 1:
          return False
        for user in results:
          users.append(cls(user))
        return users


    @classmethod
    def get_users_except_admin_like(cls,data):
        query = "SELECT * FROM users WHERE id != %(id)s and is_active = %(is_active)s and level != 9 and (first_name like %(word)s or last_name like %(word)s or email like %(word)s) limit %(offset)s,%(limit)s;"
        results = connectToMySQL('emprendeadvisor').query_db(query,data)
        users = []
        if len(results) < 1:
          return False
        for user in results:
          users.append(cls(user))
        return users

    
    @staticmethod
    def validate_password(form):
      is_valid = True 
      errors = []
      if not PASSWORD_REGEX.match(form["password"]):
        errors.append("La contraseña requiere una mayuscula, un numero y un caracter especial, debe tener entre 6 a 12 caracteres")
        is_valid = False
      return (is_valid,errors)


    @staticmethod
    def validate_update(form):
      is_valid = True 
      errors = []
      if len(form["first_name"])<3:
        errors.append("Nombre no puede estar vacio o tener menos de 3 letras")
        is_valid = False
      if len(form["last_name"])<3:
        errors.append("Apellido no puede estar vacio o tener menos de 3 letras")
        is_valid = False
      if not EMAIL_REGEX.match(form["email"]):
        errors.append("Correo invalido")
        is_valid = False
      return (is_valid,errors)

    @staticmethod
    def validate_user(user):
      is_valid = True 
      errors = []
      if len(user["first_name"])<3:
        errors.append("Nombre no puede estar vacio o tener menos de 3 letras")
        is_valid = False
      if len(user["last_name"])<3:
        errors.append("Apellido no puede estar vacio o tener menos de 3 letras")
        is_valid = False
      if not EMAIL_REGEX.match(user["email"]):
        errors.append("Correo invalido")
        is_valid = False
      data = {"email":user["email"]}
      if User.exist_mail(data):
        errors.append("Correo en uso")
        is_valid = False
      if not PASSWORD_REGEX.match(user["password"]):
        errors.append("La contraseña requiere una mayuscula, un numero y un caracter especial, debe tener entre 6 a 12 caracteres")
        is_valid = False
      if user["password"] != user["repeat_password"]:
        errors.append("Contraseñas no coinciden")
        is_valid = False
      return (is_valid,errors)

    @staticmethod
    def validate_user_update(user):
      is_valid = True 
      errors = []
      if len(user["first_name"])<3:
        errors.append("Nombre no puede estar vacio o tener menos de 3 letras")
        is_valid = False
      if len(user["last_name"])<3:
        errors.append("Apellido no puede estar vacio o tener menos de 3 letras")
        is_valid = False
      if not EMAIL_REGEX.match(user["email"]):
        errors.append("Correo invalido")
        is_valid = False
      data = {"email":user["email"]}
      if not PASSWORD_REGEX_UPDATE.match(user["password"]):
        errors.append("La contraseña requiere una mayuscula, un numero y un caracter especial, debe tener entre 6 a 12 caracteres")
        is_valid = False
      return (is_valid,errors)

    @staticmethod
    def validate_user_admin(user):
      is_valid = True 
      errors = []
      if len(user["first_name"])<3:
        errors.append("Nombre no puede estar vacio o tener menos de 3 letras")
        is_valid = False
      if len(user["last_name"])<3:
        errors.append("Apellido no puede estar vacio o tener menos de 3 letras")
        is_valid = False
      if not EMAIL_REGEX.match(user["email"]):
        errors.append("Correo invalido")
        is_valid = False
      data = {"email":user["email"]}
      if User.exist_mail(data):
        errors.append("Correo en uso")
        is_valid = False
      if not PASSWORD_REGEX.match(user["password"]):
        errors.append("La contraseña requiere una mayuscula, un numero y un caracter especial, debe tener entre 6 a 12 caracteres")
        is_valid = False
      return (is_valid,errors)