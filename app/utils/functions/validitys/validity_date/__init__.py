from datetime import datetime

def dateValidity(start:datetime,end:datetime) -> bool:
    try:
        end = parseToDatetime(end)
        start = parseToDatetime(start)

        if end > start:True
        return False

    except:return False


def parseToDatetime(date):
    try:
        new = datetime.strptime(date, "%Y-%m-%d")
        return new
    except:
        return False