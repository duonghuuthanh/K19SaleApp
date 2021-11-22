import math

from flask import render_template, request, redirect
from saleapp import app, login
import utils
from flask_login import login_user
from saleapp.admin import *


@app.route("/")
def home():
    cates = utils.load_categories()

    kw = request.args.get('keyword')
    cate_id = request.args.get('category_id')
    page = request.args.get('page', 1)
    products = utils.load_products(cate_id=cate_id, kw=kw, page=int(page))

    quantity = utils.count_products()

    return render_template('index.html',
                           categories=cates,
                           products=products,
                           pages=math.ceil(quantity/app.config['PAGE_SIZE']))


@app.route("/products")
def product_list():
    kw = request.args.get('keyword')
    from_price = request.args.get('from_price')
    to_price = request.args.get('to_price')
    cate_id = request.args.get('category_id')

    products = utils.load_products(kw=kw, from_price=from_price, to_price=to_price, cate_id=cate_id)

    return render_template('products.html',
                           products=products)


@app.route('/products/<int:product_id>')
def product_detail(product_id):
    product = utils.get_product_by_id(product_id)

    return render_template('product-details.html', product=product)


@app.route("/admin/login", methods=['post'])
def admin_login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = utils.check_user(username=username, password=password)
    if user:
        login_user(user=user)

    return redirect('/admin')


@login.user_loader
def load_user(user_id):
    return utils.get_user_by_id(user_id=user_id)


if __name__ == '__main__':
    app.run(debug=True)