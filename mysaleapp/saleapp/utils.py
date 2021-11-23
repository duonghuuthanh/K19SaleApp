import json
from saleapp import app, db
from saleapp.models import Category, Product, User
import hashlib


def read_json(path):
    with open(path, "r") as f:
        return json.load(f)


def load_categories():
    return Category.query.all()
    # return read_json(os.path.join(app.root_path, 'data/categories.json'))


def load_products(cate_id=None, kw=None, from_price=None, to_price=None, page=1):
    products = Product.query.filter(Product.active.__eq__(True))

    if cate_id:
        products = products.filter(Product.category_id.__eq__(cate_id))

    if kw:
        products = products.filter(Product.name.contains(kw))

    if from_price:
        products = products.filter(Product.price.__ge__(from_price))

    if to_price:
        products = products.filter(Product.price.__le__(to_price))

    page_size = app.config['PAGE_SIZE']
    start = (page - 1) * page_size

    return products.all()[start:start + page_size]


def count_products():
    return Product.query.filter(Product.active.__eq__(True)).count()


def get_product_by_id(product_id):
    return Product.query.get(product_id)


def get_user_by_id(user_id):
    return User.query.get(user_id)


def check_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()


def create_user(name, username, password, email=None, avatar=None):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = User(name=name.strip(),
                username=username.strip(),
                password=password,
                email=email.strip() if email else email,
                avatar=avatar)
    db.session.add(user)

    try:
        db.session.commit()
    except:
        return False
    else:
        return True
