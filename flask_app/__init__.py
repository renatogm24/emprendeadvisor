from flask import Flask
from flask_assets import Environment, Bundle
import os
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={r'*':{'origins':['https://www.emprendeadvisor.com','https://www.emprendeadvisor.com/','https://emprendeadvisor.com/','https://emprendeadvisor.com','http://127.0.0.1:5000']}})
app.config['SESSION_COOKIE_HTTPONLY'] = False
#CORS(app, support_credentials=True)
#app.config['CORS_HEADERS'] = 'Content-Type'

app.secret_key = os.environ.get("secret_key")

assets = Environment(app)

assets.url = app.static_url_path
scss = Bundle('sass/main.scss','css/styles.css', filters='libsass', output='css/all.css')
assets.register('scss_all', scss)
