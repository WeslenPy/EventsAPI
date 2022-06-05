from app.utils.functions.date_fast import actualDate
from app import db
import hashlib

class User(db.Model):
    __tablename__ = 'user'

    id  = db.Column(db.Integer, primary_key=True,autoincrement=True)
    first_name = db.Column(db.String(20),nullable=False)
    last_name = db.Column(db.String(20),nullable=False)
    balance = db.Column(db.Float(precision=2),nullable=False,default=0)
    email = db.Column(db.String(60),unique=True,nullable=False)

    cpf = db.Column(db.String(15),unique=True,default=None)

    created_at = db.Column(db.DateTime,nullable=False,default=actualDate)
    blocked_time = db.Column(db.String(40),nullable=True,default=None)
    cancellation_count = db.Column(db.Integer,nullable=False,default=0)

    
    password = db.Column(db.String(67),nullable=False)
    is_admin = db.Column(db.Boolean,default=False)
    active = db.Column(db.Boolean,default=False)
    cancellation_progress = db.Column(db.Boolean,default=False)
    purchase_progress = db.Column(db.Boolean,default=False)

    sms_user_ship = db.relationship('SmsHistory',backref=db.backref('user', lazy=True))
    cancellation_user_ship = db.relationship('CancellationPurchasedService',backref=db.backref('user', lazy=True))
    purchased_user_ship = db.relationship('PurchasedService',backref=db.backref('user', lazy=True))
    recharge_user_ship= db.relationship('RechargeHistory',backref=db.backref('user', lazy=True))
    forget_user_ship = db.relationship('ForgetPassword',backref=db.backref('user', lazy=True))

    def __init__(self,first_name,last_name,password,email,cpf=None,balance=0,blocked_time=None,active=False,
                    cancellation_count=0,is_admin=False,created_at=actualDate,cancellation_progress=False,
                    purchase_progress=False):

        self.first_name = first_name
        self.last_name = last_name
        self.password = hashlib.sha256(str.encode(password)).hexdigest()
        self.email = email
        self.balance = balance
        self.created_at  = created_at()
        self.blocked_time = blocked_time
        self.active = active
        self.cancellation_count = cancellation_count
        self.cpf= cpf
        self.is_admin = is_admin
        self.purchase_progress = purchase_progress
        self.cancellation_progress = cancellation_progress
    
    def __repr__(self) -> str:
        return self.first_name
        
