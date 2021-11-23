import math
from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user
from saleapp import app, login
import utils
import cloudinary.uploader


@app.route("/")
def home():
    cate_id = request.args.get('category_id')
    kw = request.args.get('keyword')
    page = request.args.get('page', 1)
    products = utils.load_products(cate_id=cate_id, kw=kw, page=int(page))

    return render_template('index.html',
                           products=products,
                           pages=math.ceil(utils.count_products()/app.config['PAGE_SIZE']))


@app.route("/register", methods=['get', 'post'])
def register():
    error_msg = ""
    if request.method.__eq__('POST'):
        try:
            # name = request.form['name']
            # username = request.form['username']
            password = request.form['password']
            confirm = request.form['confirm']
            # email = request.form.get('email')

            if password.__eq__(confirm):
                data = request.form.copy()
                del data['confirm']

                file = request.files['avatar']
                if file:
                    res = cloudinary.uploader.upload(file)
                    data['avatar'] = res['secure_url']

                if utils.create_user(**data):
                    redirect(url_for('signin'))
                else:
                    error_msg = "Chuong trinh dang co loi! Vui long quay lai sau!"
            else:
                error_msg = "Mat khau KHONG khop!"
        except Exception as ex:
            error_msg = str(ex)

    return render_template('register.html', error_msg=error_msg)


@app.route('/login', methods=['get', 'post'])
def signin():
    error_msg = ""
    if request.method.__eq__('POST'):
        try:
            username = request.form['username']
            password = request.form['password']

            user = utils.check_user(username=username, password=password)
            if user:
                login_user(user=user)

                return redirect("/")
            else:
                error_msg = "Chuong trinh dang co loi! Vui long quay lai sau!"

        except Exception as ex:
            error_msg = str(ex)

    return render_template('login.html', error_msg=error_msg)


@app.route('/logout')
def signout():
    logout_user()

    return redirect(url_for('signin'))

@app.route("/products")
def product_list():
    cate_id = request.args.get("category_id")
    kw = request.args.get("keyword")
    from_price = request.args.get("from_price")
    to_price = request.args.get("to_price")

    products = utils.load_products(cate_id=cate_id,
                                   kw=kw,
                                   from_price=from_price,
                                   to_price=to_price)

    return render_template('products.html',
                           products=products)


@app.route("/products/<int:product_id>")
def product_detail(product_id):
    product = utils.get_product_by_id(product_id)

    return render_template('product_detail.html',
                           product=product)


@app.context_processor
def common_reponse():
    return {
        'categories': utils.load_categories()
    }


@login.user_loader
def load_user(user_id):
    return utils.get_user_by_id(user_id=user_id)


if __name__ == '__main__':
    from saleapp.admin import *

    app.run(debug=True)