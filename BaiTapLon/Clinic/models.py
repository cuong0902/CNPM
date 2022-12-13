from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey, Enum
from Clinic import db, app
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as UserEnum

class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)

class UserRole(UserEnum):
    ADMIN = 1
    USER = 2
    DOCTOR = 3
    CASH = 4
    NURSE = 5

class User(BaseModel):
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100))
    email = Column(String(50))
    active = Column(Boolean, default=True)
    joined_date = Column(DateTime,default=datetime.now())
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    def __str__(self):
        return self.name

class Customer(BaseModel):
    name = Column(String(50), nullable=False)
    phone = Column(Integer, nullable=True)
    email = Column(String(100), nullable=False, unique=True)
    books = relationship('Books', cascade="all,delete", backref='customer', lazy=True)

    def __str__(self):
        return self.name

class Policy(BaseModel):
    topic = Column(String(100), nullable=False)
    content = Column(String(500), nullable=False)
    value = Column(Float)

    def __str__(self):
        return self.topic

class Medicine(BaseModel):
    name = Column(String(50), nullable=False)
    unit = Column(String(10), nullable=False)
    price = Column(Integer, nullable=False)

    def __str__(self):
        return self.name

class Books(BaseModel):
    booked_date = Column(DateTime, default=datetime.now())
    customer_id = Column(Integer, ForeignKey(Customer.id,  onupdate="CASCADE", ondelete="CASCADE"), nullable=False)

    def __str__(self):
        return self.id


class Receipt(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_date = Column(DateTime, default=datetime.now())
    status = Column(Integer, default=0)
    details = relationship('ReceiptDetails', backref='receipt', lazy=True)

    def __str__(self):
        return self.id


class ReceiptDetails(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)
    medicine_id = Column(Integer, ForeignKey(Medicine.id), nullable=False)
    quantity = Column(Integer, default=0)
    unit_price = Column(Float, default=0)

    def __str__(self):
        return self.id

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # c1 = Category(name='Điện thoại')
        # c2 = Category(name='Máy tính bảng')
        # c3 = Category(name='Phụ kiện')
        #
        # db.session.add_all([c1, c2, c3])
        # db.session.commit()
        # medicine = [{
        #          "id": 1,
        #          "name": "Paracetamol",
        #          "unit": "100",
        #          "price": 12000,
        #
        #         }, {
        #          "id": 2,
        #          "name": "Alexan",
        #          "unit": "78",
        #          "price": 5000,
        #
        #         }, {
        #          "id": 3,
        #          "name": "Betadine",
        #          "unit": "65",
        #          "price": 2400,
        #
        #
        #         }]
        # for m in medicine:
        #     med = Medicine(name=m['name'],
        #                    price=m['price'],
        #                   unit=m['unit']
        #                   )
        #     db.session.add(med)
        # db.session.commit()
