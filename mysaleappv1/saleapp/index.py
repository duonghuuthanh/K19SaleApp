import math

from flask import render_template, request, redirect, url_for
from saleapp import app, login
import utils
from flask_login import login_user, logout_user
import cloudinary.uploader
from saleapp.admin import *


@app.route("/")
def home():
    kw = request.args.get('keyword')
    cate_id = request.args.get('category_id')
    page = request.args.get('page', 1)
    products = utils.load_products(cate_id=cate_id, kw=kw, page=int(page))

    quantity = utils.count_products()

    return render_template('index.html',
                           products=products,
                           pages=math.ceil(quantity/app.config['PAGE_SIZE']))


@app.route('/register', methods=['get', 'post'])
def register():
    err_msg = ''
    if request.method.__eq__('POST'):
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        email = request.form.get('email')

        if password.strip().__eq__(confirm.strip()):
            file = request.files.get('avatar')
            avatar = None
            if file:
                res = cloudinary.uploader.upload(file)
                avatar = res['secure_url']

            try:
                utils.add_user(name=name, password=password,
                               username=username, email=email,
                               avatar=avatar)

                return redirect(url_for('signin'))
            except Exception as ex:
                err_msg = 'Da co loi xay ra: ' + str(ex)
        else:
            err_msg = 'Mat khau KHONG khop!'

    return render_template('register.html', err_msg=err_msg)


@app.route('/user-login', methods=['get', 'post'])
def signin():
    err_msg = ''
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        user = utils.check_user(username=username, password=password)
        if user:
            login_user(user=user)
            return redirect(url_for('home'))
        else:
            err_msg = 'Username hoac password khong chinh xac!!!'

    return render_template('login.html', err_msg=err_msg)


@app.route('/user-logout')
def signout():
    logout_user()
    return redirect(url_for('signin'))


@app.context_processor
def common_attribute():
    return {
        'categories': utils.load_categories()
    }


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