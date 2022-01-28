from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r"^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$])[\w\d@#$]{8,25}$")

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO users (first_name, last_name, email , password, created_at, updated_at ) VALUES ( %(first_name)s , %(last_name)s ,%(email)s ,%(password)s ,NOW() , NOW() );"
        return connectToMySQL('dojo_chat').query_db( query, data )

    @classmethod
    def get_user_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('dojo_chat').query_db(query,data)
        if len(results) < 1:
          return False
        return cls(results[0])

    @classmethod
    def get_user_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL('dojo_chat').query_db(query,data)
        if len(results) < 1:
          return False
        return cls(results[0])

    @classmethod
    def get_users_except_id(cls,data):
        query = "SELECT * FROM users WHERE id != %(id)s;"
        results = connectToMySQL('dojo_chat').query_db(query,data)
        users = []
        if len(results) < 1:
          return False
        for user in results:
          users.append(cls(user))
        return users

    @classmethod
    def exist_mail(cls,data):
        query = "SELECT * FROM users where email = %(email)s;"
        results = connectToMySQL('dojo_chat').query_db(query,data)
        print(results)
        if len(results) == 0:
          return False
        else:
          return True

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
