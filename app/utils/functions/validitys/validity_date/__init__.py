from datetime import datetime

def dateValidity(start:str,end:str,format="%Y-%m-%dT%H:%M:%S") -> bool:
    try:

        end:datetime = parseToDatetime(end,format)
        start:datetime = parseToDatetime(start,format)

        if end > start:return True
        return False

    except:
        return False


def parseToDatetime(date,format):
    try:
        new = datetime.strptime(date,format )
        return new
    except Exception as erro:
        print(erro)
        return False