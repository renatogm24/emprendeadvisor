from flask import Flask
from flask_assets import Environment, Bundle
import os
from flask_cors import CORS

app = Flask(__name__)

CORS(app, support_credentials=True)

app.secret_key = os.environ.get("secret_key")

S3_BUCKET = "emprendeadvisor"

app.config['S3_BUCKET'] = S3_BUCKET
app.config['S3_KEY'] = os.environ.get("AWS_ACCESS_KEY")
app.config['S3_SECRET'] = os.environ.get("AWS_ACCESS_SECRET")
app.config['S3_LOCATION'] = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)

assets = Environment(app)

assets.url = app.static_url_path
assets.debug = True
scss = Bundle('sass/main.scss','css/styles.css', filters='libsass' ,output='css/all.css')
assets.register('scss_all', scss)
