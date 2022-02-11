from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Report:
    def __init__( self , data ):
        self.id = data['id']
        self.review_id = data['review_id']
        self.comment = data['comment']
        self.text = data['text']

    def get_info_raw(self):
      data = {
          'id': self.id,
          'comment': self.comment,
          'text': self.text,
      }
      return data
    
    @classmethod
    def get_reports(cls, data ):
        query = "SELECT * FROM reports left join reviews on reports.review_id = reviews.id limit %(offset)s,%(limit)s;"
        results = connectToMySQL('emprendeadvisor').query_db( query, data )
        reports = []
        if not results:
            return False
        else:
            for report in results:
                reports.append(cls(report))
        return reports

    @classmethod
    def get_report_by_id(cls, data ):
        query = "SELECT * FROM reports left join reviews on reports.review_id = reviews.id where reports.id = %(id)s;"
        results = connectToMySQL('emprendeadvisor').query_db( query, data )
        if not results:
            return False
        else:
            return cls(results[0])

    @classmethod
    def delete_by_id(cls, data ):
        query = "DELETE FROM reports where id = %(id)s;"
        connectToMySQL('emprendeadvisor').query_db( query, data )