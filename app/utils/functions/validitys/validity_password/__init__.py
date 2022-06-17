from hashlib import sha256



def comparePassword(compare,origin):
    if sha256(str.encode(compare)).hexdigest() == origin:
        return True
    return False