from saleapp.models import Category, Product, User, UserRole
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose, Admin, AdminIndexView
from flask_login import logout_user, current_user
from flask import redirect, request
from saleapp import db, app, utils
from datetime import datetime


class AdminAutheticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class ProductView(AdminAutheticatedView):
    can_export = True
    column_filters = ['name', 'price']
    column_searchable_list = ['name']


class LogoutView(BaseView):
    @expose("/")
    def index(self):
        logout_user()

        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated


class StatsView(BaseView):
    @expose("/")
    def index(self):
        kw = request.args.get('kw')
        from_date = request.args.get('from_date')
        to_date = request.args.get('to_date')
        year = request.args.get('year', datetime.now().year)

        return self.render('admin/stats.html',
                           month_stats=utils.product_month_stats(year=year),
                           stats=utils.product_stats(kw=kw,
                                                     from_date=from_date,
                                                     to_date=to_date))

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        stats = utils.cate_stats()
        return self.render('admin/index.html', stats=stats)


admin = Admin(app=app,
              name='QUẢN TRỊ HÀNG TRỰC TUYẾN',
              template_mode='bootstrap4',
              index_view=MyAdminIndexView())

admin.add_view(AdminAutheticatedView(Category, db.session, name="Danh mục"))
admin.add_view(ProductView(Product, db.session, name="Sản phẩm"))
admin.add_view(AdminAutheticatedView(User, db.session))
admin.add_view(StatsView(name="Thong ke bao cao"))
admin.add_view(LogoutView(name="Dang xuat"))