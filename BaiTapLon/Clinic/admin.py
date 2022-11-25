from Clinic import app, db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
# from Clinic.models import Category, Product


admin = Admin(app=app, name="Quản Lý Phòng Mạch Tư", template_mode='bootstrap4')

class ProductView(ModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    # column_searchable_list = ['name','description']
    # column_filters = ['name','price']
    # column_exclude_list = ['image', 'active']
    # column_labels = {
    #     'name': 'Ten Sp',
    #     'description': 'Mo ta',
    #     'price': 'Gia',
    #     'category': 'Danh muc'
    # }
    # column_sortable_list = ['id','name','price']
# admin.add_view(ModelView(Category, db.session))
# admin.add_view(ProductView(Product, db.session))