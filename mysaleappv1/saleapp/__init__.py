from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = '$%^DFGHTYUIUY#$%^&*)(*&^%$%^&*(*&DFGHNMGHJ(*&^'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:12345678@localhost/labsaleappit02?charset=utf8mb4'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config['PAGE_SIZE'] = 8

db = SQLAlchemy(app=app)

admin = Admin(app=app, name='QUẢN TRỊ HÀNG TRỰC TUYẾN', template_mode='bootstrap4')

login = LoginManager(app=app)