import bcrypt,base64,hashlib

def comparePassword(check_password:str,actual_password:str):
    return  bcrypt.checkpw(base64.b64encode(hashlib.sha256(str.encode(check_password)).digest()),
                            str.encode(actual_password))