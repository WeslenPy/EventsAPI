from datetime import datetime

def dateValidity(start:str,end:str) -> bool:
    try:

        end:datetime = parseToDatetime(end)
        start:datetime = parseToDatetime(start)

        if end > start:return True
        return False

    except:
        return False


def parseToDatetime(date):
    try:
        new = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
        return new
    except:
        return False