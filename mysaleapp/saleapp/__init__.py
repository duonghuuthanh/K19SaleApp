from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import cloudinary

app = Flask(__name__)
app.secret_key = '@#$%^876$%^&*OIUYTRTYUIJHG^&*((*&^$%^&*'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:12345678@localhost/labsaledb?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['PAGE_SIZE'] = 8

db = SQLAlchemy(app=app)

login = LoginManager(app=app)

cloudinary.config(cloud_name='dxxwcby8l',
                  api_key='448651448423589',
                  api_secret='ftGud0r1TTqp0CGp5tjwNmkAm-A')
#
# "cloud_name": parsed_url.hostname,
# "api_key": parsed_url.username,
# "api_secret": parsed_url.password,
