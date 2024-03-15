from flask import Flask
from flask_cors import CORS

app = Flask(__name__, template_folder='D:\\Redxcel\\week4\\joins\\static\\html')
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = '0d4919d5282548adacba2fa0ab91103a'
