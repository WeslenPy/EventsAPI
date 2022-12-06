from datetime import datetime

def dateValidity(start:str,end:str,hour:str,format:str="%Y-%m-%dT%H:%M:%S") -> bool:
    try:

        end:datetime = parseToDatetime(end,format)
        start:datetime = parseToDatetime(start,format)
        hour:datetime  = parseToDatetime(hour,format)

        if end > start:return True
        return False

    except Exception as erro:
        return False


def parseToDatetime(date:str,format:str):
    try:
        new = datetime.strptime(date,format )
        return new
    except Exception as erro:
        return False