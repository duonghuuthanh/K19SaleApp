import json, os
from saleapp import app, db
from saleapp.models import Category, Product, User, Receipt, ReceiptDetail
from flask_login import current_user
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