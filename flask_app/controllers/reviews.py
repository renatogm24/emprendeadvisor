from flask import render_template, request, redirect, flash, session, jsonify, url_for
from flask_app.models import user, category, emprendimiento as empModel, review
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/like/<int:id>')
def like_review(id):
  newReview = review.Review.get_by_id({"id":id})
  user_session_id = session["user_id"]
  if newReview.user_id == user_session_id:
    return jsonify({"error":True})
  else:
    if review.Review.exist({"user_id":user_session_id,"review_id":id}):
      review.Review.delete({"user_id":user_session_id,"review_id":id})
    else:
      review.Review.like({"user_id":user_session_id,"review_id":id})
  response = {
      "updated" : True, 
    }
  return jsonify(response)