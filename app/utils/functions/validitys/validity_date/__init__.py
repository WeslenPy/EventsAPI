from datetime import datetime
from marshmallow import ValidationError

def dateValidity(start:datetime,end:datetime) -> bool:

    if end < start:raise ValidationError('end_date is invalid','end_date')
    return False

   
