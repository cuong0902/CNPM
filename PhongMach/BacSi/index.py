from BacSi import doctor
from flask import render_template
import dao

@doctor.route("/")
def home():
    DanhMuc = dao.load_DanhMuc()
    return render_template('index.html',
                           DanhMuc=DanhMuc)

