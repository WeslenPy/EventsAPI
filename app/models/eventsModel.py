from app.utils.functions.date_fast import actualDate
from app import db

class Events(db.Model):
    __tablename__ = 'events'

    id  = db.Column(db.Integer, primary_key=True,autoincrement=True)
    
    name = db.Column(db.String(255),nullable=False)
    image = db.Column(db.String(255),nullable=False)
    video = db.Column(db.String(255),nullable=False)
    # category = db.Column(db.String(255),nullable=False)
    
    cep = db.Column(db.String(30),nullable=False)
    state = db.Column(db.String(30),nullable=False)
    address = db.Column(db.String(60),nullable=False)
    number_address = db.Column(db.BigInteger,nullable=True)
    
    complement = db.Column(db.String(255),nullable=False)
    district = db.Column(db.String(60),nullable=False)
    city = db.Column(db.String(60),nullable=False)
    
    start_date = db.Column(db.DateTime,nullable=False)
    end_date = db.Column(db.DateTime,nullable=False)
    created_at = db.Column(db.DateTime,nullable=False,default=actualDate)
    
    active = db.Column(db.Boolean,default=False)

    def __init__(self,name,image,video,cep,address,number_address,state,
                 complement,district,city,start_date,end_date,active=False,created_at=actualDate):

        self.number_address= number_address
        self.created_at  = created_at()
        self.complement = complement
        self.start_date = start_date
        self.end_date = end_date
        self.district = district
        self.address = address
        self.active = active
        self.image = image
        self.video = video
        self.state = state
        self.name = name
        self.city = city
        self.cep = cep
    
    def __repr__(self) -> str:
        return self.first_name
        
