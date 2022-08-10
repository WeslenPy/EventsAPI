

def parseMessage(message:dict):
    msg = ''
    for m in message:msg = f"field {m} {message[m][0].lower()}"
    return msg

    