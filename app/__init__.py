from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

CORS(app, support_credentials=True)

from app import routes