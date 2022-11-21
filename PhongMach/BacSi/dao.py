import json, os
from BacSi import doctor

def read_json(path):
    with open(path, "r") as f:
        return json.load(f)
def load_DanhMuc():
    return read_json(os.path.join(doctor.root_path,'Data/DanhMuc.json'))