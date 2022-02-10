from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user, image

class Review:
    def __init__( self , data ):
        self.id = data['id']
        self.rating = data['rating']
        self.title = data['title']
        self.departamento = data['departamento']
        self.provincia = data["provincia"]
        self.distrito = data["distrito"]
        self.comment = data["comment"]
        self.emprendimiento_id = data["emprendimiento_id"]
        self.user_id = data["user_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user = ""
        self.emprendimiento = ""
        if "likesCount" in data:
          self.likesCount = data["likesCount"]
        else:
          self.likesCount = 0
        self.isLikedBySession = False
        self.images = ""

    def get_info_raw(self):
      data = {
          'id': self.id,
          'rating': self.rating,
          'title': self.title,
          'departamento': self.departamento,
          'provincia': self.provincia,
          'distrito' : self.distrito,
          'comment' : self.comment,
          'emprendimiento_id' : self.emprendimiento_id,
          'user_id' : self.user_id,
          'created_at' : self.created_at,
          'updated_at' : self.updated_at,
          'likesCount' : self.likesCount,
          'isLikedBySession': self.isLikedBySession
      }
      return data

    def get_info_raw_w_user(self):

      if self.images == []:
        imagesAux = []
      else:
        imagesAux = list(map( lambda x : x.get_info_raw(), self.images ))

      data = {
          'id': self.id,
          'rating': self.rating,
          'title': self.title,
          'departamento': self.departamento,
          'provincia': self.provincia,
          'distrito' : self.distrito,
          'comment' : self.comment,
          'emprendimiento_id' : self.emprendimiento_id,
          'user_id' : self.user_id,
          'created_at' : self.created_at,
          'updated_at' : self.updated_at,
          'likesCount' : self.likesCount,
          'isLikedBySession': self.isLikedBySession,
          'user' : self.user.get_info_raw(),
          'images' : imagesAux
      }
      return data
    
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO reviews (rating, title, departamento , provincia, distrito, comment, emprendimiento_id, user_id, created_at, updated_at ) VALUES ( %(rating)s , %(title)s ,%(departamento)s ,%(provincia)s, %(distrito)s , %(comment)s ,%(emprendimiento_id)s ,%(user_id)s, NOW(), NOW());"
        return connectToMySQL('emprendeadvisor').query_db( query, data )

    @classmethod
    def createReport(cls, data ):
        query = "INSERT INTO reports (text, review_id, user_id ) VALUES ( %(text)s , %(review_id)s ,%(user_id)s);"
        return connectToMySQL('emprendeadvisor').query_db( query, data )

    @classmethod
    def list_reviews_by_id(cls, data):
        if "rating" not in data or data["rating"] == "0":
          query = "SELECT *, count(l.id) as likesCount FROM reviews r left join likes l on r.id = l.review_id where r.emprendimiento_id = %(id)s group by r.id order by r.created_at DESC limit %(offset)s,%(limit)s;"
        else:
          query = "SELECT *, count(l.id) as likesCount FROM reviews r left join likes l on r.id = l.review_id where r.emprendimiento_id = %(id)s and r.rating = %(rating)s group by r.id order by r.created_at DESC limit %(offset)s,%(limit)s;"
        results = connectToMySQL('emprendeadvisor').query_db( query, data )
        if not results:
          return False
        else:
          reviews = []
          for review in results:
            newReview = cls(review)
            newReview.user = user.User.get_user_by_id({"id": newReview.user_id})
            imagesAux = image.Image.get_images_by_review_id({"id":newReview.id})
            if not imagesAux:
              newReview.images = []
            else:
              newReview.images = imagesAux
            if cls.exist({"user_id":data["user_session_id"],"review_id":newReview.id}):
              newReview.isLikedBySession = True
            reviews.append(newReview)
        return reviews

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM reviews where id = %(id)s;"
        results = connectToMySQL('emprendeadvisor').query_db( query, data )
        if not results:
          return False
        else:
          review = cls(results[0])
        return review

    @classmethod
    def exist(cls, data):
        query = "SELECT * FROM likes where user_id = %(user_id)s and review_id = %(review_id)s;"
        results = connectToMySQL('emprendeadvisor').query_db( query, data )
        if not results:
          return False
        else:
          return True

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM likes where user_id = %(user_id)s and review_id = %(review_id)s;"
        connectToMySQL('emprendeadvisor').query_db( query, data )

    @classmethod
    def like(cls, data):
        query = "INSERT INTO likes (user_id,review_id) values (%(user_id)s,%(review_id)s);"
        connectToMySQL('emprendeadvisor').query_db( query, data )

    @classmethod
    def get_opiniones(cls, data):
        query = "SELECT *, count(rating) as ratingGroup FROM reviews where emprendimiento_id = %(id)s group by rating;"
        results = connectToMySQL('emprendeadvisor').query_db( query, data )
        data = {
          "5":0,
          "4":0,
          "3":0,
          "2":0,
          "1":0,
        }
        if not results:
          return data
        else:
          totalCount = 0
          for result in results:
            if result["rating"] == 5:
              totalCount += result["ratingGroup"]
            if result["rating"] == 4:
              totalCount += result["ratingGroup"]
            if result["rating"] == 3:
              totalCount += result["ratingGroup"]
            if result["rating"] == 2:
              totalCount += result["ratingGroup"]
            if result["rating"] == 1:
              totalCount += result["ratingGroup"]
          for result in results:
            if result["rating"] == 5:
              data["5"] = result["ratingGroup"]/totalCount*100
            if result["rating"] == 4:
              data["4"] = result["ratingGroup"]/totalCount*100
            if result["rating"] == 3:
              data["3"] = result["ratingGroup"]/totalCount*100
            if result["rating"] == 2:
              data["2"] = result["ratingGroup"]/totalCount*100
            if result["rating"] == 1:
              data["1"] = result["ratingGroup"]/totalCount*100
        return data

    @staticmethod
    def validate(form):
      is_valid = True 
      errors = []
      if form["rating"] == "0":
        errors.append("Tiene que elegir un puntaje")
        is_valid = False
      if len(form["title"])<3:
        errors.append("El titulo no puede tener menos de 3 caracteres")
        is_valid = False
      if form["departamento"] == "":
        errors.append("Debes elegir un departamento")
        is_valid = False
      if form["provincia"] == "":
        errors.append("Debes elegir un provincia")
        is_valid = False
      if form["distrito"] == "":
        errors.append("Debes elegir un distrito")
        is_valid = False
      if len(form["comment"])<5:
        errors.append("El comentario no puede tener menos de 5 caracteres")
        is_valid = False
      return (is_valid,errors)
    
    