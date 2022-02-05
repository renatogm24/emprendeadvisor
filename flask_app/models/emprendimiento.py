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
        self.fbid = data['fbid']
        self.biography = data['biography']
        self.external_url = data['external_url']
        self.edge_followed_by = data['edge_followed_by']
        self.is_business_account = data['is_business_account']
        self.business_address_json = data['business_address_json']
        self.business_email = data['business_email']
        self.business_phone_number = data['business_phone_number']
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
    
    @classmethod
    def search_by_username(cls, data ):
        query = "SELECT * from emprendimientos where username = %(username)s;"
        results = connectToMySQL('emprendeadvisor').query_db( query, data )
        if not results or len(results)<1:
          return False
        else:
          return results[0]