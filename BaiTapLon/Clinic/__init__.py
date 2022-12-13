from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
import cloudinary

app = Flask(__name__)

app.secret_key = 'asdvcj@#aodfsjo46as4df'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%s@localhost/clinic?charset=utf8mb4' % quote('Admin@123')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config['PAGE_SIZE'] = 8
db = SQLAlchemy(app=app)

BOOKING_MAX = 2
cloudinary.config(
    cloud_name = 'dhwmewesm',
    api_key = '264487892914516',
    api_secret='gDPF-vECQ9oaGOCyTPsxIfoPuDU'
)