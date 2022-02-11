from flask import Flask
from flask_assets import Environment, Bundle
import os
from flask_cors import CORS
from flask_mail import Mail, Message

app = Flask(__name__)

CORS(app, support_credentials=True)

app.secret_key = os.environ.get("secret_key")
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

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

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": os.environ.get("YOUR_GMAIL"),
    "MAIL_PASSWORD": os.environ.get("YOUR_PASSWORD")
}

app.config.update(mail_settings)


