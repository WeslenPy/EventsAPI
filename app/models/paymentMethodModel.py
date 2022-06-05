from app import db


class PaymentMethod(db.Model):
    __tablename__ = 'payment_method'

    id  = db.Column(db.Integer, primary_key=True,autoincrement=True)
    method = db.Column(db.String(45),nullable=False,unique=True)
    minimun_recharge = db.Column(db.Float(precision=2),nullable=False)

    recharge_payment_ship = db.relationship('RechargeHistory',backref=db.backref('payment_method', lazy=True))

    def __init__(self,method):
    
        self.method = method

    
    def __repr__(self) -> str:
        return self.method



