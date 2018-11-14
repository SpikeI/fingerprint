from flask import Flask
from flask_cors import CORS
from flask_session import Session
from config import *

app = Flask(__name__)
app.config.from_object('config.Development')
CORS(app)
Session(app)

from views.fingerprint import fingerprint
from database import db
from model import *
from view import *

app.register_blueprint(fingerprint, url_prefix='/fingerprint')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
