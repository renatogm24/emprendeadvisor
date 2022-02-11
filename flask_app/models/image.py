from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Image:
    def __init__( self , data ):
        self.id = data['id']
        self.url = data['url']
        self.review_id = data['review_id']
        self.emprendimiento_id = data['emprendimiento_id']

    def get_info_raw(self):
      data = {
          'id': self.id,
          'url': self.url,
          'review_id': self.review_id,
          'emprendimiento_id': self.emprendimiento_id,
      }
      return data
    
    @classmethod
    def save_profile_image(cls, data ):
        query = "INSERT INTO images (url) VALUES ( %(url)s );"
        return connectToMySQL('emprendeadvisor').query_db( query, data )

    @classmethod
    def save_review_image(cls, data ):
        query = "INSERT INTO images (url, review_id) VALUES ( %(url)s, %(review_id)s );"
        return connectToMySQL('emprendeadvisor').query_db( query, data )

    @classmethod
    def delete_image_by_url(cls, data ):
        query = "DELETE FROM images where url = %(url)s;"
        return connectToMySQL('emprendeadvisor').query_db( query, data )

    @classmethod
    def delete_image_by_review(cls, data ):
        query = "DELETE FROM images where review_id = %(review_id)s;"
        return connectToMySQL('emprendeadvisor').query_db( query, data )

    @classmethod
    def get_images_by_review_id(cls, data ):
        query = "SELECT * FROM images where review_id = %(id)s ;"
        results = connectToMySQL('emprendeadvisor').query_db( query, data )
        images = []
        if not results:
            return False
        else:
            for image in results:
                images.append(cls(image))
        return images