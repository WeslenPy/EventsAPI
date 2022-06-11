from hashlib import sha256

def encryptPassword(password):
    return sha256(str.encode(password)).hexdigest()