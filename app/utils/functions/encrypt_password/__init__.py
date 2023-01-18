import bcrypt,hashlib,base64

def encryptPassword(password):
    return bcrypt.hashpw(base64.b64encode(hashlib.sha256(str.encode(password)).digest()),
                            bcrypt.gensalt())