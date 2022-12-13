import math

import cloudinary
from flask_login import login_user,logout_user
from pymysql import Time

from Clinic import app, BOOKING_MAX
from datetime import datetime as dt, time
from flask import render_template, request, redirect, url_for,jsonify
import dao
import json
from Clinic.models import User, Customer

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/aboutus")
def about_us():

    return render_template('layout/aboutus.html')
@app.route("/register_schelu")
def register_cus():
    return render_template('register-cus.html')
#


# Log out
@app.route("/user-logout")
def user_logout_exe():
    logout_user()

    return redirect("/")

@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/user-profile')
def user_profile():
    return render_template("user-profile.html")

@app.route("/admin-login", methods=["post"])
def login_admin():
    username = request.form['username']
    password = request.form['password']

    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user=user)

    return redirect('/admin')




@app.route('/register', methods=['get','post'])
def register():
    err_msg = ''
    if request.method == 'POST':
        password = request.form['password']
        confirm = request.form['confirm']
        if password.__eq__(confirm):
            avatar = ''
            if request.files:
                res = cloudinary.uploader.upload(request.files['avatar'])
                avatar = res['secure_url']

            try:
                dao.register(name=request.form['name'],
                             password=password,
                             username=request.form['username'], avatar=avatar)

                return redirect('/login')
            except:
                err_msg = 'Đã có lỗi xảy ra! Vui lòng quay lại sau!'
        else:
            err_msg = 'Mật khẩu KHÔNG khớp!'

    return render_template('register.html', err_msg=err_msg)

@app.route("/api/check-booking-date", methods=["post"])
def check_booking_date():
    date = request.form.get("bookingdate")
    if dt.strptime(date, '%d/%m/%Y') > dt.now():
        return jsonify(True)
    return jsonify(False)


@app.route("/api/check-booking-time", methods=["post"])
def check_booking_time():
    booking_time = request.form.get("bookingtime")
    booking_time = dt.strptime(booking_time, '%I:%M %p').time()
    if booking_time < time(8, 0, 0) or booking_time > time(19, 0, 0) \
            or time(13, 0, 0) > booking_time > time(12, 0, 0):
        return jsonify(False)
    return jsonify(True)

@app.route("/api/add-booking", methods=["post"])
def add_booking():
    books = {
        "name": request.form.get("bookingname", current_user.patient.name if current_user.is_authenticated else ""),
        "email": request.form.get("bookingemail", current_user.patient.name if current_user.is_authenticated else ""),
        "date": request.form.get("bookingdate")
    }

    books["date"] = dt.strptime(books["date"], '%d/%m/%Y')

    period = dt.strptime(request.form.get("bookingtime"), '%I:%M %p').hour
    period = f"{period:02d}:00 - {period + 1:02d}:00"
    booking_time = Time.query.filter(Time.period == period).first()

    if dao.get_amount_of_people(booking_time, books["date"]) == BOOKING_MAX:
        return jsonify({"message": "Maximum of people!"}), 400

    books["time"] = booking_time

    if dao.add_booking(**books):
        return jsonify({
            "message": "booking successfully!",
            "amount": dao.get_amount_of_people(booking_time, books["date"])
        }), 200

    return jsonify({"message": "can't add booking!"}), 404


if __name__ == '__main__':
    from Clinic.admin import *
    app.run(debug=True)
