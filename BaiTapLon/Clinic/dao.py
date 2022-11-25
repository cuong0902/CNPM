# from Clinic import app, db
# import json, os,hashlib
# from Clinic.models import  User
#
# def read_json(path):
#     with open(path, "r") as f:
#         return json.load(f)
#
# def load_category():
#     # return read_json(os.path.join(app.root_path, 'Data/category.json'))
#     return Category.query.all()
#
# def load_product(kw=None,cate_id=None,page=1):
#     products = Product.query.filter(Product.active.__eq__(True))
#     if cate_id:
#         products = Product.query.filter(Product.category_id.__eq__(cate_id))
#     if kw:
#         products = Product.query.filter(Product.name.contains(kw))
#     page_size = app.config['PAGE_SIZE']
#     start = (page - 1) * page_size
#     end = start + page_size
#
#     return products.slice(start, end).all()
#     # product = read_json(os.path.join(app.root_path, 'Data/product.json'))
#     # if(cate_id):
#     #     product = [p for p in product if p['category_id'] == int(cate_id)]
#     # if kw:
#     #     product = [p for p in product if p['name'].lower().find(kw.lower()) >= 0]
#     # return product
#
# def count_product():
#     return Product.query.filter(Product.active.__eq__(True)).count()
#
# def add_user(name,username, password, **kwargs):
#     password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
#     user = User(name=name.strip(),
#                 username=username.strip(),
#                 password=password,
#                 email=kwargs.get('email'),
#                 avatar=kwargs.get('avatar'))
#     db.session.add(user)
#     db.session.commit()
#
# def get_product_byid(product_id):
#     return Product.query.get(product_id)
#     # product = read_json(os.path.join(app.root_path, 'Data/product.json'))
#     # for p in product:
#     #     if p['id'] == product_id:
#     #         return p