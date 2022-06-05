from app.utils.functions.date_fast import expirationTime,actualDate
from app import db


class ForgetPassword(db.Model):
    __tablename__ = 'forget_password'


    id  = db.Column(db.Integer, primary_key=True,autoincrement=True)
    url = db.Column(db.String(255), unique=True,nullable=False)
    expires = db.Column(db.String(40),nullable=False,default=lambda:expirationTime({'minutes':30}))
    email = db.Column(db.String(60),unique=True,nullable=False)

    created_at = db.Column(db.DateTime,nullable=False,default=actualDate)
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)

    status = db.Column(db.Boolean,nullable=False)


    def __init__(self,url,status,expires,email,user_id,created_at=actualDate):
    
        self.url = url
        self.status = status
        self.expires = expires
        self.email = email
        self.created_at  = created_at()

        self.user_id = user_id
    


