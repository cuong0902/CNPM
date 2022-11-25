import math
from Clinic import app
from flask import render_template, request, redirect, url_for
import dao


@app.route("/")
def home():

    # kw = request.args.get('keyword')
    # page = request.args.get('pages', 1)

    # counter = dao.count_product()
    return render_template('index.html')

                           # page= math.ceil(counter/app.config['PAGE_SIZE'])
@app.route("/aboutus")
def about_us():

    return render_template('layout/aboutus.html')

#
@app.route('/register', methods=['get','post'])
def user_register():
    err_msg = ""
    if request.method.__eq__('POST'):
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        confirm = request.form.get('confirm')

        try:
            if password.strip().__eq__(confirm.strip()):
                dao.add_user(name=name,
                             username=username,
                             password=password,
                             email=email)
                return redirect(url_for('home'))
            else:
                err_msg = 'Mat Khau khong khop!!!'
        except Exception as ex:
            err_msg = "He Thong Dang Co Loi " + str(ex)

    return render_template('register.html',err_msg=err_msg)




if __name__ == '__main__':
    from Clinic.admin import *
    app.run(debug=True)