from app.utils.functions.date_fast import expirationTime,actualDate
from app import db




class PurchasedService(db.Model):
    __tablename__ = 'purchased_service'

    id  = db.Column(db.Integer, primary_key=True,autoincrement=True)
    price = db.Column(db.Float(precision=2),nullable=False)

    status = db.Column(db.String(60),nullable=False)
    service_number = db.Column(db.String(60),nullable=False)
    created_at = db.Column(db.DateTime,nullable=False,default=actualDate)

    expiration = db.Column(db.String(40),nullable=False,default=lambda:expirationTime({"minutes":18}))

    user_id = db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
    service_id = db.Column(db.Integer,db.ForeignKey("service.id"),nullable=False)
    server_api = db.Column(db.Integer,db.ForeignKey("api.id"),nullable=False)
    operator_id = db.Column(db.Integer,db.ForeignKey("operator.id"),nullable=False)

    activation_id = db.Column(db.String(45),nullable=False)

    sms_purchased_ship = db.relationship('SmsHistory',
                                         backref=db.backref('purchased_service', lazy=True))
    
    cancellation_purchased_ship = db.relationship('CancellationPurchasedService',
                                                  backref=db.backref('purchased_service', lazy=True))

    def __init__(self,price,status,service_number,user_id,service_id,server_api,activation_id,operator_id,
                created_at=actualDate):
    
        self.price = price
        self.status = status
        self.expiration = expirationTime({'minutes':18})
        self.service_number= service_number
        self.user_id= user_id
        self.created_at  = created_at()
        self.server_api = server_api
        self.operator_id = operator_id

        self.service_id= service_id
        self.activation_id= activation_id

    
    def __repr__(self) -> str:
        return str(self.service_number)