from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey, Enum
from Clinic import db, app
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as UserEnum

class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


class Account(BaseModel):
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100))
    email = Column(String(50))
    active = Column(Boolean, default=True)
    joined_date = Column(DateTime,default=datetime.now())

    def __str__(self):
        return self.name



class TaiKhoanAdmin(Account):
    __tablename__= 'Account'
    name = Column(String(50), nullable=False)
    phone = Column(Integer, nullable=True)
    def __str__(self):
        return self.name

class Bacsi(BaseModel):
    __tablename__= 'Bác Sĩ'
    admin_id = Column(Integer, ForeignKey(TaiKhoanAdmin.id), nullable=False)
    def __str__(self):
        return self.name

class YTa(BaseModel):
    __tablename__= 'Y Tá'
    admin_id = Column(Integer, ForeignKey(TaiKhoanAdmin.id), nullable=False)
    def __str__(self):
        return self.name

class ThuNgan(BaseModel):
    __tablename__= 'Thu Ngân'
    admin_id = Column(Integer, ForeignKey(TaiKhoanAdmin.id), nullable=False)
    def __str__(self):
        return self.name

class QuanTri(BaseModel):
    __tablename__= 'Quản Trị'
    admin_id = Column(Integer, ForeignKey(TaiKhoanAdmin.id), nullable=False)
    def __str__(self):
        return self.name

class TaiKhoanUser(Account):
    __tablename__= 'User'
    def __str__(self):
        return self.name

class DanhSachKham(BaseModel):
    __tablename__ = 'Danh Sách Khám'
    HoTen = Column(String(50), nullable=False)
    NgayKham = Column(DateTime, default=datetime.now())
    YTa_id = Column(Integer, ForeignKey(YTa.id), nullable=False)

    def __str__(self):
        return self.name

class BenhNhan(BaseModel):
    __tablename__= 'Bệnh Nhân'
    name = Column(String(50), nullable=False)
    phone = Column(Integer, nullable=True)
    email = Column(String(100), nullable=False, unique=True)
    DiaChi = Column(String(100), nullable=False)
    id_user = Column(Integer, ForeignKey(TaiKhoanUser.id), nullable=False, unique=True)
    lichkham_id = Column(Integer, ForeignKey(DanhSachKham.id), nullable=False, unique=True)
    def __str__(self):
        return self.name

class PhieuKham(BaseModel):
    __tablename__= 'Phiếu Khám'
    name = Column(String(50), nullable=False)
    NgayKham = Column(DateTime, default=datetime.now())
    TrieuChung = Column(String(500), nullable=False)
    Bacsi_id = Column(Integer, ForeignKey(Bacsi.id), nullable=False)
    def __str__(self):
        return self.name

class HoaDon(BaseModel):
    __tablename__= 'Hóa Đơn'
    NgayTao = Column(DateTime, default=datetime.now())
    TienKham = Column(Float, nullable=False)
    TienThuoc = Column(Float, nullable=False)
    ThuNgan_id = Column(Integer, ForeignKey(ThuNgan.id), nullable=False)
    Toa_Thuoc = relationship('ToaThuoc', backref='hoa don thuoc', lazy=True)
    def __str__(self):
        return self.name

class Thuoc(BaseModel):
    __tablename__= 'Thuốc'
    name = Column(String(50), nullable=False)
    NgaySanXuat = Column(DateTime, default=datetime.now())
    DonVi = Column(String(500), nullable=False)
    hoadon_id = Column(Integer, ForeignKey(HoaDon.id), nullable=False)
    def __str__(self):
        return self.name

class ToaThuoc(BaseModel):
    __tablename__= 'Toa Thuốc'
    name = Column(String(50), nullable=False)
    SoLuong = Column(Integer, nullable=False)
    CachDung = Column(String(500), nullable=False)
    Thuoc_id = Column(Integer, ForeignKey(Thuoc.id), nullable=False)
    PhieuKham_id = Column(Integer, ForeignKey(PhieuKham.id), nullable=False)
    def __str__(self):
        return self.name

class QuyDinh(BaseModel):
    __tablename__ = 'Quy Dinh'
    QuanTri_id = Column(Integer, ForeignKey(QuanTri.id), nullable=False)
    name = Column(String(50), nullable=False)
    LoaiQuyDinh = Column(String(100), nullable=False)
    NoiDung = Column(String(500), nullable=False)
    NgayQuyDinh = Column(DateTime, default=datetime.now())
    NgayKetThuc = Column(DateTime, default=datetime.now())

    def __str__(self):
        return self.topic

class QuyDinhThuoc(BaseModel):
    __tablename__ = 'Quy Dinh Thuoc'
    Gia = Column(Integer, nullable=False)
    Thuoc_id = Column(Integer, ForeignKey(Thuoc.id), nullable=False)
    QuanTri_id = Column(Integer, ForeignKey(QuanTri.id), nullable=False)

    def __str__(self):
        return self.name


class HoSoBenhAn(BaseModel):
    __tablename__= 'Hồ Sơ Bệnh Án'
    HoTen = Column(String(50), nullable=False)
    TienSuBenh = Column(String(500), nullable=False)
    BenhNhan_id = Column(Integer, ForeignKey(BenhNhan.id), nullable=False)
    def __str__(self):
        return self.name


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # c1 = Category(name='Điện thoại')
        # c2 = Category(name='Máy tính bảng')
        # c3 = Category(name='Phụ kiện')
        #
        # db.session.add_all([c1, c2, c3])
        # db.session.commit()
        # product = [{
        #          "id": 1,
        #          "name": "iPhone 13 Pro Max",
        #          "description": "Apple, 128GB, RAM: 6GB, iOS13",
        #          "price": 17000000,
        #          "image": "images/iphone-13-pro-xanh-xa-1.png",
        #          "category_id": 1
        #         }, {
        #          "id": 2,
        #          "name": "Oppo Reno 6 5G",
        #          "description": "Oppo, 128GB, RAM: 6GB",
        #          "price": 37000000,
        #          "image": "images/oppo-reno6-den-1-org.png",
        #          "category_id": 1
        #         }, {
        #          "id": 3,
        #          "name": "Galaxy Tab A7s",
        #          "description": "Samsung, 64GB, RAM: 6GB",
        #          "price": 24000000,
        #          "image": "images/samsung-galaxy-tab-a7-lite-1-3-org.png",
        #          "category_id": 2
        #         }]
        # for p in product:
        #     pro = Product(name=p['name'], price=p['price'],
        #                   description=p['description'],
        #                   category_id=p['category_id'],
        #                   image=p['image'])
        #     db.session.add(pro)
        # db.session.commit()
