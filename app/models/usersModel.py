from app.utils.functions.date_fast import actualDate
from app import db
import hashlib

class Users(db.Model):
    __tablename__ = 'users'

    id  = db.Column(db.Integer, primary_key=True,autoincrement=True)
    
    email = db.Column(db.String(60),unique=True,nullable=False)
    password = db.Column(db.String(67),nullable=False)
    
    phone = db.Column(db.String(14),unique=True,nullable=False)
    cep = db.Column(db.String(30),nullable=False)
    address = db.Column(db.String(60),nullable=False)
    number_address = db.Column(db.BigInteger,nullable=True)
    
    complement = db.Column(db.String(255),nullable=False)
    district = db.Column(db.String(60),nullable=False)
    state = db.Column(db.String(60),nullable=False)
    city = db.Column(db.String(60),nullable=False)
    genre = db.Column(db.String(60),nullable=False)
    
    created_at = db.Column(db.DateTime,nullable=False,default=actualDate)
    is_admin = db.Column(db.Boolean,default=False)
    active = db.Column(db.Boolean,default=False)

    def __init__(self,first_name,last_name,password,email,phone,cep,address,number_address,
                 complement,district,city,is_admin=False,active=False,created_at=actualDate):

        self.password = hashlib.sha256(str.encode(password)).hexdigest()
        self.number_address= number_address
        self.created_at  = created_at()
        self.complement = complement
        self.first_name = first_name
        self.last_name = last_name
        self.district = district
        self.is_admin = is_admin
        self.address = address
        self.active = active
        self.email = email
        self.phone = phone
        self.city = city
        self.cep = cep
    
    def __repr__(self) -> str:
        return self.first_name
        
