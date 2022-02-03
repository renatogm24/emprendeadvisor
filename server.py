from flask_app.controllers import controller, users, admin
from flask_app import app

if __name__ == "__main__":
    app.run(debug=True,port=80)