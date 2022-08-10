

def parseMessage(message):
    msg = ''
    for m in message:
        msg = f"field {m} {message[m][0]}"
    return msg

    