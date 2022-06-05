from datetime import datetime,timedelta

def actualDate():
    now=  datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    return datetime.strptime(now, '%d-%m-%Y %H:%M:%S')

def expirationTime(expires):
    return float(datetime.timestamp(datetime.now()+timedelta(**expires)))

def actualTimeStamp():
    return datetime.timestamp(datetime.now())

