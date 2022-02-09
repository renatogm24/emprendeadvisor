from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user

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

    @classmethod
    def list_reviews_by_id(cls, data):
        query = "SELECT *, count(l.id) as likesCount FROM reviews r left join likes l on r.id = l.review_id where r.emprendimiento_id = %(id)s group by r.id limit %(offset)s,%(limit)s;"
        results = connectToMySQL('emprendeadvisor').query_db( query, data )
        if not results:
          return False
        else:
          reviews = []
          for review in results:
            newReview = cls(review)
            newReview.user = user.User.get_user_by_id({"id": newReview.user_id})
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
    
    # @classmethod
    # def save_category(cls, data ):
    #     if data["category_id"] == "0":
    #       query = "INSERT INTO categories (name, is_active, level) VALUES ( %(name)s, %(is_active)s, %(level)s  );"
    #     else:
    #       query = "INSERT INTO categories (name, is_active, category_id, level) VALUES ( %(name)s, %(is_active)s, %(category_id)s, %(level)s  );"
    #     return connectToMySQL('emprendeadvisor').query_db( query, data )

    # @classmethod
    # def updateCategoryAll(cls, data ):
    #     if data["category_id"] == "0":
    #       query = "UPDATE categories SET name = %(name)s  WHERE id = %(id)s;"
    #     else:
    #       query = "UPDATE categories SET name = %(name)s ,category_id = %(category_id)s WHERE id = %(id)s;"
    #     return connectToMySQL('emprendeadvisor').query_db( query, data )

    # @classmethod
    # def approveCategory(cls, data ):
    #     query = "UPDATE categories SET is_active = 1 WHERE category_id = %(id)s or id = %(id)s;"
    #     return connectToMySQL('emprendeadvisor').query_db( query, data )

    # @classmethod
    # def delete_category(cls, data ):
    #     query = "DELETE FROM categories where id = %(id)s;"
    #     return connectToMySQL('emprendeadvisor').query_db( query, data )

    # @classmethod
    # def delete_subcategories(cls, data ):
    #     query = "DELETE FROM categories where category_id = %(id)s;"
    #     return connectToMySQL('emprendeadvisor').query_db( query, data )
    
    # @classmethod
    # def exist_category(cls, data ):
    #     if data["category_id"] == "0":
    #       query = "SELECT * FROM categories c1 left join categories c2 on c1.category_id = c2.id where c1.name = %(name)s and c2.id is NULL;"
    #     else:
    #       query = "SELECT * FROM categories c1 left join categories c2 on c1.category_id = c2.id where c1.name = %(name)s and c2.id = %(category_id)s;"
    #     result = connectToMySQL('emprendeadvisor').query_db( query, data )
    #     if not result:
    #       result = False
    #     else:
    #       result = True
    #     return result

    # @classmethod
    # def list_categories(cls, data ):
    #     if data["is_active"] != 0:
    #       if data["category_id"] == "":
    #         query = "SELECT * FROM categories c1 left join categories c2 on c1.category_id = c2.id left join emprendimientos emp on c1.id = emp.category_id where c1.is_active = %(is_active)s and c1.level = %(level)s and c2.name is NULL group by c1.id limit %(offset)s,%(limit)s;"
    #       else:
    #         query = "SELECT * FROM categories c1 left join categories c2 on c1.category_id = c2.id left join emprendimientos emp on c1.id = emp.category_id where c1.is_active = %(is_active)s and c1.level = %(level)s and c1.category_id = %(category_id)s group by c1.id limit %(offset)s,%(limit)s;"
    #     else:
    #       if data["category_id"] == "":
    #         query = "SELECT * FROM categories c1 left join categories c2 on c1.category_id = c2.id left join emprendimientos emp on c1.id = emp.category_id where c1.is_active = %(is_active)s  group by c1.id limit %(offset)s,%(limit)s;"
    #       else:
    #         query = "SELECT * FROM categories c1 left join categories c2 on c1.category_id = c2.id left join emprendimientos emp on c1.id = emp.category_id where c1.is_active = %(is_active)s  and c1.category_id = %(category_id)s group by c1.id limit %(offset)s,%(limit)s;"
        
    #     results = connectToMySQL('emprendeadvisor').query_db( query, data )
    #     if not results:
    #       return False
    #     else:
    #       categories = []
    #       for categorie in results:
    #         newCategory = cls(categorie)
    #         if "username" in categorie:
    #             newCategory.emprendimiento = categorie["username"]
    #         categories.append(newCategory)
    #     return categories

    # @classmethod
    # def list_all_categories(cls ):        
    #     query = "SELECT * FROM categories where level = 1 and is_active = 1;"
    #     results = connectToMySQL('emprendeadvisor').query_db( query)
    #     if not results:
    #       return False
    #     else:
    #       categories = []
    #       for categorie in results:
    #         categories.append(cls(categorie))
    #     return categories

    # @classmethod
    # def get_category_by_name(cls, data ):        
    #     query = "SELECT * FROM categories where level = 1 and name = %(name)s ;"
    #     results = connectToMySQL('emprendeadvisor').query_db( query, data)
    #     if not results:
    #       return False
    #     else:
    #       category = cls(results[0])
    #     return category

    # @classmethod
    # def get_category_by_id(cls, data ):        
    #     query = "SELECT * FROM categories c1 left join categories c2 on c1.category_id = c2.id where c1.id = %(id)s ;"
    #     results = connectToMySQL('emprendeadvisor').query_db( query, data)
    #     if not results:
    #       return False
    #     else:
    #       category = cls(results[0])
    #       category.padre = results[0]["c2.name"]
    #     return category

    # @classmethod
    # def list_subcategories(cls, data ):        
    #     query = "SELECT * FROM categories where level = 2 and category_id = %(id)s and is_active = 1;"
    #     results = connectToMySQL('emprendeadvisor').query_db( query, data)
    #     if not results:
    #       return False
    #     else:
    #       categories = []
    #       for categorie in results:
    #         categories.append(cls(categorie))
    #     return categories

    # @classmethod
    # def list_all_categories_with_subcategories(cls):
    #     query = "SELECT * FROM categories c1 left join categories c2 on c1.category_id = c2.id where c1.level = 2 and c1.is_active = 1;"
    #     results = connectToMySQL('emprendeadvisor').query_db( query)
    #     if not results:
    #       return False
    #     else:
    #       categories = []
    #       for categorie in results:
    #         exists = False
    #         index = 0
    #         found = ""
    #         for cataux in categories:
    #           if cataux.id == categorie["category_id"]:
    #             exists = True
    #             found = index
    #           index +=1
    #         if exists:
    #           dataSub = {
    #             "id" : categorie["id"],
    #             "name" : categorie["name"],
    #             "is_active" : categorie["is_active"],
    #             "category_id" : categorie["category_id"],
    #             "level" : categorie["level"],
    #           }
    #           categories[found].subcategories.append(cls(dataSub))
    #         else:
    #           dataCat = {
    #             "id" : categorie["c2.id"],
    #             "name" : categorie["c2.name"],
    #             "is_active" : categorie["c2.is_active"],
    #             "category_id" : categorie["c2.category_id"],
    #             "level" : categorie["c2.level"],
    #           }
    #           categoryObj = cls(dataCat)
    #           dataSub = {
    #             "id" : categorie["id"],
    #             "name" : categorie["name"],
    #             "is_active" : categorie["is_active"],
    #             "category_id" : categorie["category_id"],
    #             "level" : categorie["level"],
    #           }
    #           categoryObj.subcategories.append(cls(dataSub))
    #           categories.append(categoryObj)
    #     return categories

    # @classmethod
    # def get_category(cls, data ):
    #     query = "SELECT * FROM categories where id = %(id)s;"
    #     result = connectToMySQL('emprendeadvisor').query_db( query, data )
    #     if not result:
    #       return result
    #     else:
    #       result = cls(result[0])
    #     return result

    # @classmethod
    # def get_categories_like(cls,data):
    #     if data["category_id"] == "":
    #       query = "SELECT * FROM categories WHERE is_active = %(is_active)s and level = %(level)s and category_id is NULL and (name like %(word)s ) limit %(offset)s,%(limit)s;"
    #     else:
    #       query = "SELECT * FROM categories WHERE is_active = %(is_active)s and level = %(level)s and category_id = %(category_id)s and (name like %(word)s ) limit %(offset)s,%(limit)s;"
    #     results = connectToMySQL('emprendeadvisor').query_db(query,data)
    #     categories = []
    #     if len(results) < 1:
    #       return False
    #     for category in results:
    #       categories.append(cls(category))
    #     return categories

    # @staticmethod
    # def validate_category(category):
    #   is_valid = True 
    #   errors = []
    #   print(category["level"])
    #   if category["level"] == "1":        
    #     print(category["category_id"])
    #     if category["category_id"] != "0":
    #       errors.append("Categoria 1 no puede depender de otra Categoria 1")
    #       is_valid = False
    #   if category["level"] == "2":  
    #     if category["category_id"] == "0":
    #       errors.append("Subcategoria debe tener una categoria padre")
    #       is_valid = False
    #   if len(category["name"])<1:
    #     errors.append("Nombre no puede ser vacio")
    #     is_valid = False
    #   if Category.exist_category(category):
    #     errors.append("Categoría existente")
    #     is_valid = False
    #   return (is_valid,errors)