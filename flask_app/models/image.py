from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Image:
    def __init__( self , data ):
        self.id = data['id']
        self.url = data['url']
        self.review_id = data['review_id']
        self.emprendimiento_id = data['emprendimiento_id']
    
    @classmethod
    def save_profile_image(cls, data ):
        query = "INSERT INTO images (url) VALUES ( %(url)s );"
        return connectToMySQL('emprendeadvisor').query_db( query, data )

    @classmethod
    def delete_image_by_url(cls, data ):
        query = "DELETE FROM images where url = %(url)s;"
        return connectToMySQL('emprendeadvisor').query_db( query, data )