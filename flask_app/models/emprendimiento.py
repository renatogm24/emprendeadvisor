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
        if "promedio" in data:
          self.promedio = data['promedio']
        else:
          self.promedio = 0
        if "cuenta" in data:
          self.cuenta = data['cuenta']
        else:
          self.cuenta = 0

    def get_info_raw(self):
      data = {
          'id': self.id,
          'username': self.username,
          'full_name': self.full_name,
          'biography': self.biography,
          'external_url': self.external_url,
          'follower_count': self.follower_count,
          'is_business': self.is_business,
          'public_email': self.public_email,
          'contact_phone_number': self.contact_phone_number,
          'category_name': self.category_name,
          'is_private': self.is_private,
          'profile_pic_url': self.profile_pic_url,
          'profile_pic_url_hd': self.biography,
          'category_id': self.category_id,
          'url_p1': self.url_p1,
          'url_p2': self.url_p2,
          'promedio': self.promedio,
          'cuenta': self.cuenta,
          'categoria': "",
          'subcategoria': "",
      }
      return data
    
    @classmethod
    def search_by_username(cls, data ):
        query = "SELECT * from emprendimientos left join categories on emprendimientos.category_id = categories.id where username = %(username)s and categories.is_active = 1;"
        results = connectToMySQL('emprendeadvisor').query_db( query, data )
        if not results or len(results)<1:
          return False
        else:
          return results[0]

    @classmethod
    def search_by_id(cls, data ):
        query = "SELECT e.id, e.username, IFNULL(avg(r.rating),0) as promedio, IFNULL(count(r.rating),0) as cuenta, e.full_name, e.biography, e.external_url, e.follower_count, e.is_business, e.public_email, e.contact_phone_number, e.category_name, e.is_private, e.profile_pic_url, e.profile_pic_url_hd, e.category_id, e.created_at, e.updated_at FROM emprendimientos e left join reviews r on e.id = r.emprendimiento_id left join categories c on e.category_id = c.id where e.id = %(id)s and c.is_active = 1 group by e.id;"
        results = connectToMySQL('emprendeadvisor').query_db( query, data )
        if not results or len(results)<1:
          return False
        else:
          return results[0]

    @classmethod
    def save(cls, data ):
        query = "INSERT INTO emprendimientos (`username`,`full_name`,`biography`,`external_url`,`follower_count`,`is_business`,`public_email`,`contact_phone_number`,`category_name`,`is_private`,`profile_pic_url`,`profile_pic_url_hd`,`category_id`,`created_at`,`updated_at` ) VALUES (%(username)s,%(full_name)s,%(biography)s,%(external_url)s,%(follower_count)s,%(is_business)s,%(public_email)s,%(contact_phone_number)s,%(category_name)s,%(is_private)s,%(profile_pic_url)s,%(profile_pic_url_hd)s,%(category_id)s,NOW(),NOW());"
        return connectToMySQL('emprendeadvisor').query_db( query, data )

    @classmethod
    def delete(cls, data ):
        query = "DELETE emprendimientos FROM emprendimientos left join categories on emprendimientos.category_id = categories.id where emprendimientos.category_id = %(id)s or categories.category_id = %(id)s;"
        return connectToMySQL('emprendeadvisor').query_db( query, data )

    @classmethod
    def delete_emprendimiento_by_id(cls, data ):
        query = "DELETE emprendimientos FROM emprendimientos where id = %(id)s;"
        return connectToMySQL('emprendeadvisor').query_db( query, data )

    @classmethod
    def get_emprendimientos(cls, data):
        if "category_id" not in data:
          if "min_promedio" not in data:
            query = "SELECT e.id, e.username, IFNULL(round(avg(r.rating),1),0) as promedio, IFNULL(count(r.rating),0) as cuenta, e.full_name, e.biography, e.external_url, e.follower_count, e.is_business, e.public_email, e.contact_phone_number, e.category_name, e.is_private, e.profile_pic_url, e.profile_pic_url_hd, e.category_id, e.created_at, e.updated_at FROM emprendimientos e left join reviews r on e.id = r.emprendimiento_id left join categories c on e.category_id = c.id where c.is_active = 1 group by id order by {order_by} DESC limit {offset},{limit};".format(**data)
          else:
            query = "SELECT e.id, e.username, IFNULL(round(avg(r.rating),1),0) as promedio, IFNULL(count(r.rating),0) as cuenta, e.full_name, e.biography, e.external_url, e.follower_count, e.is_business, e.public_email, e.contact_phone_number, e.category_name, e.is_private, e.profile_pic_url, e.profile_pic_url_hd, e.category_id, e.created_at, e.updated_at FROM emprendimientos e left join reviews r on e.id = r.emprendimiento_id left join categories c on e.category_id = c.id where c.is_active = 1 group by id having promedio between {min_promedio} and {max_promedio} and cuenta between {min_reviews} and {max_reviews} and e.follower_count between {min_followers} and {max_followers} order by {order_by} DESC limit {offset},{limit};".format(**data)
        else:
          if "min_promedio" not in data:
            query = "SELECT e.id, e.username, IFNULL(round(avg(r.rating),1),0) as promedio, IFNULL(count(r.rating),0) as cuenta, e.full_name, e.biography, e.external_url, e.follower_count, e.is_business, e.public_email, e.contact_phone_number, e.category_name, e.is_private, e.profile_pic_url, e.profile_pic_url_hd, e.category_id, e.created_at, e.updated_at FROM emprendimientos e left join reviews r on e.id = r.emprendimiento_id left join categories c on e.category_id = c.id where c.is_active = 1 and e.category_id = {category_id} or c.category_id = {category_id} group by id order by {order_by} DESC limit {offset},{limit};".format(**data)
          else:
            query = "SELECT e.id, e.username, IFNULL(round(avg(r.rating),1),0) as promedio, IFNULL(count(r.rating),0) as cuenta, e.full_name, e.biography, e.external_url, e.follower_count, e.is_business, e.public_email, e.contact_phone_number, e.category_name, e.is_private, e.profile_pic_url, e.profile_pic_url_hd, e.category_id, e.created_at, e.updated_at FROM emprendimientos e left join reviews r on e.id = r.emprendimiento_id left join categories c on e.category_id = c.id where c.is_active = 1 and e.category_id = {category_id} or c.category_id = {category_id} group by id having promedio between {min_promedio} and {max_promedio} and cuenta between {min_reviews} and {max_reviews} and e.follower_count between {min_followers} and {max_followers} order by {order_by} DESC limit {offset},{limit};".format(**data)
        
        results = connectToMySQL('emprendeadvisor').query_db(query)
        emprendimientos = []
        if not results:
          return False
        for emp in results:
          emprendimientos.append(cls(emp))
        return emprendimientos

    @classmethod
    def get_emprendimientos_admin(cls, data):
        query = "SELECT e.id, e.username, IFNULL(round(avg(r.rating),1),0) as promedio, IFNULL(count(r.rating),0) as cuenta, e.full_name, e.biography, e.external_url, e.follower_count, e.is_business, e.public_email, e.contact_phone_number, e.category_name, e.is_private, e.profile_pic_url, e.profile_pic_url_hd, e.category_id, e.created_at, e.updated_at FROM emprendimientos e left join reviews r on e.id = r.emprendimiento_id left join categories c on e.category_id = c.id group by id limit {offset},{limit};".format(**data)
        results = connectToMySQL('emprendeadvisor').query_db(query)
        emprendimientos = []
        if not results:
          return False
        for emp in results:
          emprendimientos.append(cls(emp))
        return emprendimientos

    @classmethod
    def get_emprendimientos_like_admin(cls, data):
        query = "SELECT e.id, e.username, IFNULL(round(avg(r.rating),1),0) as promedio, IFNULL(count(r.rating),0) as cuenta, e.full_name, e.biography, e.external_url, e.follower_count, e.is_business, e.public_email, e.contact_phone_number, e.category_name, e.is_private, e.profile_pic_url, e.profile_pic_url_hd, e.category_id, e.created_at, e.updated_at FROM emprendimientos e left join reviews r on e.id = r.emprendimiento_id left join categories c on e.category_id = c.id where (e.username like {word} ) group by id limit {offset},{limit};".format(**data)
        results = connectToMySQL('emprendeadvisor').query_db(query)
        emprendimientos = []
        if not results:
          return False
        for emp in results:
          emprendimientos.append(cls(emp))
        return emprendimientos
    
    @classmethod
    def get_emprendimientos_max_min(cls, data):
        if "category_id" not in data:
          query = "select max(subtable.promedio) as max_promedio, min(subtable.promedio) as min_promedio, max(subtable.cuenta) as max_reviews, min(subtable.cuenta) as min_reviews, max(subtable.follower_count) as max_followers, min(subtable.follower_count) as min_followers from (  SELECT e.id, e.username, IFNULL(avg(r.rating),0) as promedio, IFNULL(count(r.rating),0) as cuenta, e.full_name, e.biography, e.external_url, e.follower_count, e.is_business, e.public_email, e.contact_phone_number, e.category_name, e.is_private, e.profile_pic_url, e.profile_pic_url_hd, e.category_id, e.created_at, e.updated_at FROM emprendimientos e left join reviews r on e.id = r.emprendimiento_id left join categories c on e.category_id = c.id where c.is_active = 1 group by id order by promedio DESC) as subtable;"
        else:
          query = "select max(subtable.promedio) as max_promedio, min(subtable.promedio) as min_promedio, max(subtable.cuenta) as max_reviews, min(subtable.cuenta) as min_reviews, max(subtable.follower_count) as max_followers, min(subtable.follower_count) as min_followers from (  SELECT e.id, e.username, IFNULL(avg(r.rating),0) as promedio, IFNULL(count(r.rating),0) as cuenta, e.full_name, e.biography, e.external_url, e.follower_count, e.is_business, e.public_email, e.contact_phone_number, e.category_name, e.is_private, e.profile_pic_url, e.profile_pic_url_hd, e.category_id, e.created_at, e.updated_at FROM emprendimientos e left join reviews r on e.id = r.emprendimiento_id left join categories c on e.category_id = c.id where c.is_active=1 and e.category_id = %(category_id)s or c.category_id = %(category_id)s group by id order by promedio DESC) as subtable;"
        results = connectToMySQL('emprendeadvisor').query_db(query,data)
        if not results:
          return False
        result = results[0]
        data = {
          "max_promedio" : result["max_promedio"],
          "min_promedio" : result["min_promedio"],
          "max_reviews" : result["max_reviews"],
          "min_reviews" : result["min_reviews"],
          "max_followers" : result["max_followers"],
          "min_followers" : result["min_followers"],
        }
        return data

    @classmethod
    def get_emprendimientos_total_count(cls, data):
        if "category_id" not in data:
          query = "select count(*) as cuenta from emprendimientos e left join categories c on e.category_id = c.id where c.is_active = 1;"
        else:
          query = "select count(*) as cuenta from emprendimientos e left join categories c on e.category_id = c.id where c.is_active=1 and e.category_id = %(category_id)s or c.category_id = %(category_id)s;"
        results = connectToMySQL('emprendeadvisor').query_db(query, data)
        if not results:
          return False
        result = results[0]
        data = result["cuenta"]
        return data