from flask_app.config.mysqlconnection import connectToMySQL

class Category:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.is_active = data['is_active']
        self.category_id = data['category_id']
        self.level = data["level"]
        self.subcategories = []

    def get_info_raw(self):
      data = {
          'id': self.id,
          'name': self.name,
          'is_active': self.is_active,
          'category_id': self.category_id,
          'level': self.level,
      }
      return data
    
    @classmethod
    def save_category(cls, data ):
        if data["category_id"] == "0":
          query = "INSERT INTO categories (name, is_active, level) VALUES ( %(name)s, %(is_active)s, %(level)s  );"
        else:
          query = "INSERT INTO categories (name, is_active, category_id, level) VALUES ( %(name)s, %(is_active)s, %(category_id)s, %(level)s  );"
        return connectToMySQL('emprendeadvisor').query_db( query, data )

    @classmethod
    def updateCategoryAll(cls, data ):
        if data["category_id"] == "0":
          query = "UPDATE categories SET name = %(name)s  WHERE id = %(id)s;"
        else:
          query = "UPDATE categories SET name = %(name)s ,category_id = %(category_id)s WHERE id = %(id)s;"
        return connectToMySQL('emprendeadvisor').query_db( query, data )

    @classmethod
    def delete_category(cls, data ):
        query = "DELETE FROM categories where id = %(id)s;"
        return connectToMySQL('emprendeadvisor').query_db( query, data )

    @classmethod
    def delete_subcategories(cls, data ):
        query = "DELETE FROM categories where category_id = %(id)s;"
        return connectToMySQL('emprendeadvisor').query_db( query, data )
    
    @classmethod
    def exist_category(cls, data ):
        if data["category_id"] == "0":
          query = "SELECT * FROM categories c1 left join categories c2 on c1.category_id = c2.id where c1.name = %(name)s and c2.id is NULL;"
        else:
          query = "SELECT * FROM categories c1 left join categories c2 on c1.category_id = c2.id where c1.name = %(name)s and c2.id = %(category_id)s;"
        result = connectToMySQL('emprendeadvisor').query_db( query, data )
        if not result:
          result = False
        else:
          result = True
        return result

    @classmethod
    def list_categories(cls, data ):
        if data["category_id"] == "":
          query = "SELECT * FROM categories c1 left join categories c2 on c1.category_id = c2.id where c1.is_active = 1 and c1.level = %(level)s and c2.name is NULL limit %(offset)s,%(limit)s;"
        else:
          query = "SELECT * FROM categories c1 left join categories c2 on c1.category_id = c2.id where c1.is_active = 1 and c1.level = %(level)s and c1.category_id = %(category_id)s limit %(offset)s,%(limit)s;"
        results = connectToMySQL('emprendeadvisor').query_db( query, data )
        if not results:
          return False
        else:
          categories = []
          for categorie in results:
            categories.append(cls(categorie))
        return categories

    @classmethod
    def list_all_categories(cls ):        
        query = "SELECT * FROM categories where level = 1;"
        results = connectToMySQL('emprendeadvisor').query_db( query)
        if not results:
          return False
        else:
          categories = []
          for categorie in results:
            categories.append(cls(categorie))
        return categories

    @classmethod
    def list_all_categories_with_subcategories(cls):
        query = "SELECT * FROM categories c1 left join categories c2 on c1.category_id = c2.id where c1.level = 2;"
        results = connectToMySQL('emprendeadvisor').query_db( query)
        if not results:
          return False
        else:
          categories = []
          for categorie in results:
            exists = False
            index = 0
            found = ""
            for cataux in categories:
              if cataux.id == categorie["category_id"]:
                exists = True
                found = index
              index +=1
            if exists:
              dataSub = {
                "id" : categorie["id"],
                "name" : categorie["name"],
                "is_active" : categorie["is_active"],
                "category_id" : categorie["category_id"],
                "level" : categorie["level"],
              }
              categories[found].subcategories.append(cls(dataSub))
            else:
              dataCat = {
                "id" : categorie["c2.id"],
                "name" : categorie["c2.name"],
                "is_active" : categorie["c2.is_active"],
                "category_id" : categorie["c2.category_id"],
                "level" : categorie["c2.level"],
              }
              categoryObj = cls(dataCat)
              dataSub = {
                "id" : categorie["id"],
                "name" : categorie["name"],
                "is_active" : categorie["is_active"],
                "category_id" : categorie["category_id"],
                "level" : categorie["level"],
              }
              categoryObj.subcategories.append(cls(dataSub))
              categories.append(categoryObj)
        return categories

    @classmethod
    def get_category(cls, data ):
        query = "SELECT * FROM categories where id = %(id)s;"
        result = connectToMySQL('emprendeadvisor').query_db( query, data )
        if not result:
          return result
        else:
          result = cls(result[0])
        return result

    @classmethod
    def get_categories_like(cls,data):
        if data["category_id"] == "":
          query = "SELECT * FROM categories WHERE is_active = %(is_active)s and level = %(level)s and category_id is NULL and (name like %(word)s ) limit %(offset)s,%(limit)s;"
        else:
          query = "SELECT * FROM categories WHERE is_active = %(is_active)s and level = %(level)s and category_id = %(category_id)s and (name like %(word)s ) limit %(offset)s,%(limit)s;"
        results = connectToMySQL('emprendeadvisor').query_db(query,data)
        categories = []
        if len(results) < 1:
          return False
        for category in results:
          categories.append(cls(category))
        return categories

    @staticmethod
    def validate_category(category):
      is_valid = True 
      errors = []
      print(category["level"])
      if category["level"] == "1":        
        print(category["category_id"])
        if category["category_id"] != "0":
          errors.append("Categoria 1 no puede depender de otra Categoria 1")
          is_valid = False
      if category["level"] == "2":  
        if category["category_id"] == "0":
          errors.append("Subcategoria debe tener una categoria padre")
          is_valid = False
      if len(category["name"])<1:
        errors.append("Nombre no puede ser vacio")
        is_valid = False
      if Category.exist_category(category):
        errors.append("Categoría existente")
        is_valid = False
      return (is_valid,errors)