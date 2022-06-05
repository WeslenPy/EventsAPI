from app.utils.functions.date_fast import expirationTime,actualDate
from app import db


class RechargeHistory(db.Model):

    __tablename__ = 'recharge_history'
    
    id  = db.Column(db.Integer, primary_key=True,autoincrement=True)
    txid = db.Column(db.String(255),nullable=False)
    value = db.Column(db.Float(precision=2),nullable=False)
    created_at = db.Column(db.DateTime,nullable=False,default=actualDate)
    payday = db.Column(db.DateTime,default=actualDate)
    expiration = db.Column(db.String(40),nullable=False,default=lambda:expirationTime({"minutes":20}))
    obs = db.Column(db.Text,nullable=False,default=None)
    url = db.Column(db.String(255),nullable=True)
    status = db.Column(db.String(30),nullable=False,default='ACTIVE')

    user_id = db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
    payment_method_id = db.Column(db.Integer,db.ForeignKey("payment_method.id"),nullable=False)


    def __init__(self,txid,value,obs,user_id,payment_method_id,url=None,status='ACTIVE',
                payday=actualDate,created_at=actualDate,expiration={"minutes":20}):
      
        self.txid = txid
        self.value = value
        self.status = status
        self.payday = payday()
        self.expiration = expirationTime(expiration)
        self.obs = obs
        self.url = url
        self.created_at =created_at()
        self.user_id = user_id
        self.payment_method_id = payment_method_id

    def __repr__(self) -> str:
        return str(self.id)

