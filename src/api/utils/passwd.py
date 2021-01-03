from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import JWTManager

def hash_password(password):
    return pbkdf2_sha256.hash(password)

def check_password(password, hashed):
    try:
        ret = pbkdf2_sha256.verify(password, hashed)
    except:
        ret = False
    return ret

jwt = JWTManager()
