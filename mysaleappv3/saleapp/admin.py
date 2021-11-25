from saleapp import admin, db
from flask_admin.contrib.sqla import ModelView
from saleapp.models import Category, Product


class ProductView(ModelView):
    column_searchable_list = ['name']
    column_filters = ['name', 'price', 'category']


admin.add_view(ModelView(Category, db.session))
admin.add_view(ProductView(Product, db.session))