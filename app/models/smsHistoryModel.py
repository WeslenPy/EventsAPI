from app.utils.functions.date_fast import actualDate
from app import db



class SmsHistory(db.Model):
    __tablename__ = 'sms_history'
    
    id  = db.Column(db.Integer, primary_key=True,autoincrement=True)
    sms = db.Column(db.Text)

    received_at = db.Column(db.DateTime,default=actualDate)
    
    purchased_service_id = db.Column(db.Integer,db.ForeignKey("purchased_service.id"))
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"))


    def __init__(self,sms,purchased_service_id,user_id,received_at=actualDate):

        self.sms = sms
        self.purchased_service_id = purchased_service_id
        self.received_at =received_at()
        self.user_id = user_id


    def __repr__(self) -> str:
        return str(self.id)