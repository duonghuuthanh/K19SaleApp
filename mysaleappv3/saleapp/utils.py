import json, os
from saleapp import app, db
from saleapp.models import Category, Product, User, Receipt, ReceiptDetail
from flask_login import current_user
from sqlalchemy import func
from sqlalchemy.sql import extract
import hashlib


def read_json(path):

    with open(path) as f:
        return json.load(f)


def read_categories():
    return Category.query.all()
    # return read_json(os.path.join(app.root_path, "data/categories.json"))


def read_products(cate_id=None, kw=None, to_price=None, from_price=None, page=1):
    products = Product.query.filter(Product.active.__eq__(True))

    if cate_id:
        products = products.filter(Product.category_id.__eq__(cate_id))

    if kw:
        products = products.filter(Product.name.contains(kw))

    if from_price:
        products = products.filter(Product.price.__ge__(float(from_price)))

    if to_price:
        products = products.filter(Product.price.__le__(float(to_price)))

    page_size = app.config['PAGE_SIZE']
    start = (page - 1) * page_size
    end = start + page_size

    return products.slice(start, end).all()


def count_products():
    return Product.query.filter(Product.active.__eq__(True)).count()


def add_user(name, username, password, **kwargs):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = User(name=name.strip(),
                username=username.strip(),
                password=password,
                email=kwargs.get('email'),
                avatar=kwargs.get('avatar'))

    db.session.add(user)
    db.session.commit()


def check_login(username, password):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

        return User.query.filter(User.username.__eq__(username.strip()),
                                 User.password.__eq__(password)).first()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def cart_stats(cart):
    total_quantity, total_amount = 0, 0

    if cart:
        for c in cart.values():
            total_quantity += c['quantity']
            total_amount += c['quantity'] * c['price']

    return {
        'total_quantity': total_quantity,
        'total_amount': total_amount
    }


def add_receipt(cart):
    if cart:
        receipt = Receipt(user=current_user)
        db.session.add(receipt)

        for c in cart.values():
            d = ReceiptDetail(receipt=receipt,
                              product_id=c['id'],
                              quantity=c['quantity'],
                              unit_price=c['price'])
            db.session.add(d)

        db.session.commit()


def category_stats():
    """
    SELECT c.id, c.name, count(p.id)
    FROM category c left outer join product p on c.id = p.category_id
    group by c.id, c.name
    """
    # return Category.query.join(Product,
    #                            Product.category_id.__eq__(Category.id), isouter=True)\
    #                .add_columns(func.count(Product.id))\
    #                .group_by(Category.id, Category.name).all()

    return db.session.query(Category.id, Category.name,
                            func.count(Product.id))\
                     .join(Product,
                           Product.category_id.__eq__(Category.id),
                           isouter=True)\
                     .group_by(Category.id, Category.name).all()


def product_stats(kw=None, from_date=None, to_date=None):
    p = db.session.query(Product.id, Product.name,
                         func.sum(ReceiptDetail.quantity * ReceiptDetail.unit_price))\
                  .join(ReceiptDetail, ReceiptDetail.product_id.__eq__(Product.id), isouter=True)\
                  .join(Receipt, Receipt.id.__eq__(ReceiptDetail.receipt_id))\
                  .group_by(Product.id, Product.name)

    if kw:
        p = p.filter(Product.name.contains(kw))

    if from_date:
        p = p.filter(Receipt.created_date.__ge__(from_date))

    if to_date:
        p = p.filter(Receipt.created_date.__le__(to_date))

    return p.all()


def product_month_stats(year):
    return db.session.query(extract('month', Receipt.created_date),
                            func.sum(ReceiptDetail.quantity*ReceiptDetail.unit_price))\
                     .join(ReceiptDetail, ReceiptDetail.receipt_id.__eq__(Receipt.id))\
                     .filter(extract('year', Receipt.created_date) == year)\
                     .group_by(extract('month', Receipt.created_date))\
                     .order_by(extract('month', Receipt.created_date)).all()
