from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto import Random
from app import app
from model import User
import base64

def encrypt(text):
    BS = 16
    pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)

    key = pad(app.config['SECRET_KEY'])
    text = pad(text)

    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(text.encode('utf-8')))


def decrypt(cipher):
    BS = 16
    pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
    unpad = lambda s: s[:-ord(s[len(s) - 1:])]

    key = pad(app.config['SECRET_KEY']).encode('utf-8')
    enc = base64.b64decode(cipher)
    iv = enc[:16]

    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc[16:]))


def get_user_num():
    count = User.query.count()
    return count


def get_user_data(page):
    page_size = app.config['INDEX_PAGE_SIZE']
    data = User.query.offset(page_size * (page - 1)).limit(page_size).all()
    return data