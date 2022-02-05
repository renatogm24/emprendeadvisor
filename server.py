from flask_app.controllers import controller, emprendimientos, users, admin
from flask_app import app

if __name__ == "__main__":
    app.run(debug=True,port=80)