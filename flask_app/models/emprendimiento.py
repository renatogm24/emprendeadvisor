from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Emprendimiento:
    def __init__( self , data ):
        if "id" in data:
          self.id = data['id']
        else:
          self.id = ""
        self.username = data['username']
        self.full_name = data['full_name']
        self.biography = data['biography']
        self.external_url = data['external_url']
        self.follower_count = data['follower_count']
        self.is_business = data['is_business']
        self.public_email = data['public_email']
        self.contact_phone_number = data['contact_phone_number']
        self.category_name = data["category_name"]
        self.is_private = data['is_private']
        self.profile_pic_url = data['profile_pic_url']
        self.profile_pic_url_hd = data['profile_pic_url_hd']
        if "created_at" in data:
          self.created_at = data['created_at']
        else:
          self.created_at = ""
        if "updated_at" in data:
          self.updated_at = data['updated_at']
        else:
          self.updated_at = ""
        if "category_id" in data:
          self.category_id = data['category_id']
        else:
          self.category_id = ""
        if "images" in data:
          self.images = data['images']
        else:
          self.images = []
        arr = data["profile_pic_url_hd"].split("?")
        self.url_p1 = arr[0]
        self.url_p2 = arr[1]
    
    @classmethod
    def search_by_username(cls, data ):
        query = "SELECT * from emprendimientos left join categories on emprendimientos.category_id = categories.id where username = %(username)s and categories.is_active = 1;"
        results = connectToMySQL('emprendeadvisor').query_db( query, data )
        if not results or len(results)<1:
          return False
        else:
          return results[0]

    @classmethod
    def save(cls, data ):
        query = "INSERT INTO emprendimientos (`username`,`full_name`,`biography`,`external_url`,`follower_count`,`is_business`,`public_email`,`contact_phone_number`,`category_name`,`is_private`,`profile_pic_url`,`profile_pic_url_hd`,`category_id`,`created_at`,`updated_at` ) VALUES (%(username)s,%(full_name)s,%(biography)s,%(external_url)s,%(follower_count)s,%(is_business)s,%(public_email)s,%(contact_phone_number)s,%(category_name)s,%(is_private)s,%(profile_pic_url)s,%(profile_pic_url_hd)s,%(category_id)s,NOW(),NOW());"
        return connectToMySQL('emprendeadvisor').query_db( query, data )