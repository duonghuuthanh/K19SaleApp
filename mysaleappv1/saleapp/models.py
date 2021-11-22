from sqlalchemy import Column, Integer, Float, String, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from saleapp import db
from datetime import datetime
from flask_login import UserMixin
from enum import Enum as UserEnum


class UserRole(UserEnum):
    ADMIN = 1
    USER = 2


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class User(BaseModel, UserMixin):
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    email = Column(String(50))
    active = Column(Boolean, default=True)
    joined_date = Column(DateTime, default=datetime.now())
    user_role = Column(Enum(UserRole), default=UserRole.USER)

    def __str__(self):
        return self.name


class Category(BaseModel):
    __tablename__ = 'category'

    name = Column(String(50), nullable=False)
    products = relationship('Product', backref='category', lazy=True)

    def __str__(self):
        return self.name


class Product(BaseModel):
    __tablename__ = 'product'

    name = Column(String(50), nullable=False)
    description = Column(String(255))
    price = Column(Float, default=0)
    image = Column(String(100))
    active = Column(Boolean, default=True)
    created_date = Column(DateTime, default=datetime.now())
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)


if __name__ == '__main__':
    db.create_all()

    # p1 = Product(name='iPhone 7 Plus', description='Apple, 32GB, RAM: 3GB, iOS13', price=17000000, image='images/p1.png', category_id=1)
    # p2 = Product(name='iPad Pro 2020', description='Apple, 128GB, RAM: 6GB', price=32000000, image='images/p2.png', category_id=1)
    # p3 = Product(name='Galaxy Note 10 Plus', description='Samsung, 64GB, RAML: 6GB', price=24000000, image='images/p3.png', category_id=2)
    # p4 = Product(name='iPhone 13 Pro Max', description='Apple, 128GB, RAM: 6GB, 2021', price=34000000, image='images/p1.png', category_id=1)
    # p5 = Product(name='iPad Mini 2020', description='Apple, 64GB', price=12000000, image='images/p3.png', category_id=2)
    #
    # db.session.add(p1)
    # db.session.add(p2)
    # db.session.add(p3)
    # db.session.add(p4)
    # db.session.add(p5)
    # db.session.commit()

    # c1 = Category(name='Dien thoai')
    # c2 = Category(name='May tinh bang')
    # c3 = Category(name='Phu kien')
    #
    # db.session.add(c1)
    # db.session.add(c2)
    # db.session.add(c3)
    #
    # db.session.commit()