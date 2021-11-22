from saleapp.models import Category, Product, User, UserRole
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask_login import logout_user, current_user
from flask import redirect
from saleapp import admin, db


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
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


admin.add_view(AdminAutheticatedView(Category, db.session, name="Danh mục"))
admin.add_view(ProductView(Product, db.session, name="Sản phẩm"))
admin.add_view(AdminAutheticatedView(User, db.session))
admin.add_view(LogoutView(name="Dang xuat"))