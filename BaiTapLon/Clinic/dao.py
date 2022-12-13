import hashlib
import hmac
import random
import string

from flask import url_for, abort
from sqlalchemy import text, func, and_
from sqlalchemy.sql.functions import count

from Clinic import app
from Clinic.models import Customer,  db, Books,  Receipt, \
    ReceiptDetails,  Medicine, User




def add_booking(name, email, date):
    try:
        if not exist_user(email):
            customer = Customer(name=name, email=email)
            db.session.add(customer)
        else:
            customer = Customer.query.filter(Customer.email == email).first()

        books = Books(booked_date=date, customer=customer)
        db.session.add(books)
        db.session.commit()

        return True
    except Exception as ex:
        print("Booking Error: " + str(ex))
        return False



def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()
def exist_user(email):
    try:
        if Customer.query.filter(Customer.email == email).first():
            return True
        return False
    except Exception as ex:
        print(ex)


def hmac_sha256(data):
    return hmac.new(app.secret_key.encode('utf-8'),
                    data.encode('utf-8'),
                    hashlib.sha256).hexdigest()



def get_amount_of_people(time, date):
    # Every period just have 2 people
    count = 0
    for book in time.books_times:
        if book.booked_date == date:
            count += 1
    return count


def get_request_payment(patient_id):
    return Receipt.query.filter(and_(Receipt.patient_id == patient_id, Receipt.status == 0)).first()


def receipt_stats(receipt):
    total_quantity, total_amount = 0, 0

    for item in receipt.details:
        total_quantity += item.quantity
        total_amount += item.quantity * item.unit_price

    return {
        "total_quantity": total_quantity,
        "total_amount": total_amount
    }


def complete_payment(receipt_id):
    try:
        receipt = Receipt.query.get(receipt_id)
        receipt.status = 1
        db.session.add(receipt)
        db.session.commit()

        return True
    except Exception as ex:
        print(ex)
        return False


# def get_records(patient_id):
#     return ClinicalRecords.query.filter(ClinicalRecords.patient_id == patient_id).all()
#


def get_all_receipts():
    return db.session.query(Receipt.created_date, Customer.name,
                            func.sum(ReceiptDetails.quantity * ReceiptDetails.unit_price).label("TotalPrice")) \
        .join(Receipt, Receipt.id == ReceiptDetails.receipt_id) \
        .join(Customer, Customer.id == Receipt.patient_id).group_by(ReceiptDetails.receipt_id, Customer.name).all()


# def get_profile_customer(name_patient=None):
#     profile = db.session.query(Receipt.created_date, Customer.name, Customer.phone,
#                                Disease.name.label("nameDis"),
#                                func.sum(ReceiptDetails.quantity * ReceiptDetails.unit_price).label("TotalPrice")) \
#         .join(Receipt, Receipt.id == ReceiptDetails.receipt_id) \
#         .join(Customer, Customer.id == Receipt.patient_id) \
#         .join(ClinicalRecords, func.DATE(ClinicalRecords.checked_date) == func.DATE(Receipt.created_date)) \
#         .join(Disease, Disease.id == ClinicalRecords.disease_id) \
#         .group_by(ReceiptDetails.receipt_id, Customer.name)
#
#     if name_patient:
#         profile = profile.filter(Customer.name.contains(name_patient))
#
#     return profile.all()


def get_name_receipt_detail(name_patient):
    detail = db.session.query(Medicine.name, ReceiptDetails.medicine_id, ReceiptDetails.quantity,
                              ReceiptDetails.unit_price, Receipt.created_date) \
        .join(Receipt, Receipt.id == ReceiptDetails.receipt_id).join(Medicine,
                                                                     Medicine.id == ReceiptDetails.medicine_id) \
        .join(Customer, Customer.id == Receipt.patient_id)

    if name_patient:
        detail = detail.filter(Customer.name.contains(name_patient))

    return detail.all()


# def get_stats_by_date(date_start=None, date_end=None):
#     stats = db.session.query(Disease.name, count(ClinicalRecords.patient_id).label("count_di")) \
#         .join(Disease, Disease.id == ClinicalRecords.disease_id)
#
#     if date_start:
#         stats = stats.filter(ClinicalRecords.checked_date.__ge__(date_start))
#
#     if date_end:
#         stats = stats.filter(ClinicalRecords.checked_date.__le__(date_end))
#
#     return stats.group_by(ClinicalRecords.disease_id).all()
#

def get_all_detail_by_date(date1=None, date2=None):
    detail_by_date = db.session.query(Receipt.created_date, Customer.name,
                                      func.sum(ReceiptDetails.quantity * ReceiptDetails.unit_price).label("TotalPrice")) \
        .join(Receipt, Receipt.id == ReceiptDetails.receipt_id) \
        .join(Customer, Customer.id == Receipt.patient_id)

    if date1:
        detail_by_date = detail_by_date.filter(Receipt.created_date.__ge__(date1))

    if date2:
        detail_by_date = detail_by_date.filter(Receipt.created_date.__le__(date2))

    return detail_by_date.group_by(ReceiptDetails.receipt_id).all()


def get_totaldetail_by_date(date1=None, date2=None):
    totaldetail_by_date = db.session.query(
        func.sum(ReceiptDetails.quantity * ReceiptDetails.unit_price).label("TotalPrice")) \
        .join(Receipt, Receipt.id == ReceiptDetails.receipt_id)

    if date1:
        totaldetail_by_date = totaldetail_by_date.filter(Receipt.created_date.__ge__(date1))

    if date2:
        totaldetail_by_date = totaldetail_by_date.filter(Receipt.created_date.__le__(date2))

    return totaldetail_by_date.all()
