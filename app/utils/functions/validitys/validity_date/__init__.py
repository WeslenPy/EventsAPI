from datetime import datetime
import traceback

def dateValidity(start:str,end:str) -> bool:
    try:

        end = parseToDatetime(end)
        start = parseToDatetime(start)

        print(end,start,file=open('./newLogError.log','a'))

        if end > start:True
        return False

    except:
        traceback.print_exc(file=open('./newLog.log','a'))
        return False


def parseToDatetime(date):
    try:
        new = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
        return new
    except:
        return False