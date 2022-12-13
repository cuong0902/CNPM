from Clinic import app, db
from flask_admin import Admin, BaseView, expose
from flask import redirect, request
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
from Clinic.models import Medicine, Policy
import dao


admin = Admin(app=app, name="Quản Lý Phòng Mạch Tư", template_mode='bootstrap4')


class AuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

class MedicineView(ModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    column_searchable_list = ['name']
    column_filters = ['name','price']
    column_exclude_list = ['image', 'active']
    column_labels = {
        'name': 'Tên Thuốc',
        'price': 'Giá',
        'unit': 'Đơn Vị',
        'id': 'Mã Thuốc'
    }
    column_sortable_list = ['id','name','price']
class PoliciyView(ModelView):
    can_view_details = True
    can_export = True
    column_labels = {
        'topic': 'Chủ Đề',
        'content': 'Nội Dung',
        'value': 'Số Lượng'
    }
class LogoutView(BaseView):
    @expose("/")
    def index(self):
        # logout_user()
        return redirect('/admin')

    # def is_accessible(self):
    #     return current_user.is_authenticated
class StatsView(BaseView):
    @expose("/")
    def index(self):
        date_start = request.args.get("date_start")
        date_end = request.args.get("date_end")
        # stats = dao.get_stats_by_date(date_start=date_start, date_end=date_end)
        # if stats:
        #     mes = "Valid data!"
        return self.render("admin/stats.html")
        # else:
        #     mes = "Invalid data!"
        #     return self.render("admin/stats.html", stats=stats, mes=mes)

    # def is_accessible(self):
    #     return current_user.is_authenticated

admin.add_view(PoliciyView(Policy, db.session, name='Quy Định'))
admin.add_view(StatsView(name="Thống Kê Báo Cáo Tháng", category="Quản Trị"))
admin.add_view(MedicineView(Medicine, db.session, name='Danh Sách Thuốc'))
admin.add_view(LogoutView(name="Đăng Xuất", endpoint="logout"))