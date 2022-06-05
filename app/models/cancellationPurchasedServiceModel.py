from app.utils.functions.date_fast import actualTimeStamp
from app import db


class CancellationPurchasedService(db.Model):
    __tablename__ = 'cancellation_purchased_service'

    id  = db.Column(db.Integer, primary_key=True,autoincrement=True)

    cancellation_time = db.Column(db.String(40),nullable=True,default=actualTimeStamp)

    user_id = db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
    purchased_service_id = db.Column(db.Integer,db.ForeignKey("purchased_service.id"),nullable=False)

    def __init__(self,user_id,purchased_service_id,cancellation_time=actualTimeStamp):
    
        self.cancellation_time =cancellation_time()
        self.user_id = user_id
        self.purchased_service_id= purchased_service_id

    def __repr__(self) -> str:
        return str(self.cancellation_time)