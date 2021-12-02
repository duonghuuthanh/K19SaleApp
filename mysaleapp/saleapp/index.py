import math

from flask import render_template, request, redirect, url_for, session, jsonify
from saleapp import app, login
import utils
import cloudinary.uploader
from flask_login import login_user, logout_user, login_required
from saleapp.admin import *
from saleapp.models import UserRole


@app.route("/")
def index():
    kw = request.args.get('keyword')
    cate_id = request.args.get('category_id')
    page = request.args.get('page', 1)

    products = utils.read_products(kw=kw, cate_id=cate_id, page=int(page))
    counter = utils.count_products()

    return render_template("index.html",
                           products=products,
                           pages=math.ceil(counter/app.config['PAGE_SIZE']))


@app.route('/register', methods=['get', 'post'])
def user_register():
    err_msg = ""
    if request.method.__eq__('POST'):
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        confirm = request.form.get('confirm')
        avatar_path = None

        try:
            if password.strip().__eq__(confirm.strip()):
                avatar = request.files.get('avatar')
                if avatar:
                    res = cloudinary.uploader.upload(avatar)
                    avatar_path = res['secure_url']

                utils.add_user(name=name, username=username,
                               password=password, email=email,
                               avatar=avatar_path)
                return redirect(url_for('user_signin'))
            else:
                err_msg = 'Mat khau KHONG khop!!!'
        except Exception as ex:
            err_msg = 'He thong dang co loi: ' + str(ex)

    return render_template('register.html', err_msg=err_msg)


@app.route('/user-login', methods=['get', 'post'])
def user_signin():
    err_msg = ''
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = utils.check_login(username=username, password=password)
        if user:
            login_user(user=user)

            return redirect(url_for(request.args.get('next', 'index')))
        else:
            err_msg = 'Username hoac password KHONG chinh xac!!!'

    return render_template('login.html', err_msg=err_msg)


@app.route('/user-logout')
def user_signout():
    logout_user()
    return redirect(url_for('user_signin'))


@app.route('/admin-login', methods=['post'])
def signin_admin():
    username = request.form['username']
    password = request.form['password']

    user = utils.check_login(username=username,
                            password=password)
    if user:
        login_user(user=user)

    return redirect('/admin')


@app.context_processor
def common_response():
    return {
        'categories': utils.read_categories(),
        'cart_stats': utils.cart_stats(session.get('cart'))
    }


@login.user_loader
def user_load(user_id):
    return utils.get_user_by_id(user_id=user_id)


@app.route("/products")
def product_list():
    cate_id = request.args.get('category_id')
    kw = request.args.get('keyword')
    from_price = request.args.get('from_price')
    to_price = request.args.get('to_price')

    products = utils.read_products(cate_id=cate_id, kw=kw,
                                   from_price=from_price, to_price=to_price)

    return render_template('product_list.html', products=products)


@app.route('/cart')
def cart():
    return render_template('cart.html',
                           cart_stats=utils.cart_stats(session.get('cart')))


@app.route('/api/add-to-cart', methods=['post'])
def add_to_cart():
    data = request.json
    id = str(data.get('id'))
    name = data.get('name')
    price = data.get('price')

    cart = session.get('cart')
    if not cart:
        cart = {}

    if id in cart:
        cart[id]['quantity'] = cart[id]['quantity'] + 1
    else:
        cart[id] = {
            'id': id,
            'name': name,
            'price': price,
            'quantity': 1
        }

    session['cart'] = cart

    return jsonify(utils.cart_stats(session.get('cart')))


@app.route('/api/update-cart', methods=['put'])
def update_cart():
    id = str(request.json.get('id'))
    quantity = request.json.get('quantity')

    cart = session.get('cart')
    err_msg = ''
    if cart:
        if id in cart:
            cart[id]['quantity'] = quantity
            session['cart'] = cart

            return jsonify({
                'code': 200,
                'data': utils.cart_stats(cart)
            })
        else:
            err_msg = 'Khong co san pham tuong ung de cap nhat!'
    else:
        err_msg = 'Chua co gio hang!'

    return jsonify({
        'code': 404,
        'err_msg': err_msg
    })


@app.route('/api/delete-cart/<product_id>', methods=['delete'])
def delete_cart(product_id):
    cart = session.get('cart')
    err_msg = ''
    if cart:
        if product_id in cart:
            del cart[product_id]
            session['cart'] = cart

            return jsonify({
                'code': 200,
                'data': utils.cart_stats(cart)
            })
        else:
            err_msg = 'Khong co san pham tuong ung de cap nhat!'
    else:
        err_msg = 'Chua co gio hang!'

    return jsonify({
        'code': 404,
        'err_msg': err_msg
    })


@app.route('/api/pay', methods=['post'])
@login_required
def pay():
    try:
        utils.add_receipt(session.get('cart'))
        del session['cart']
    except:
        return jsonify({'code': 404})

    return jsonify({'code': 200})


if __name__ == '__main__':
    app.run(debug=True)