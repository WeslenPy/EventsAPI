from app.utils.functions.date_fast import actualDate
from app import db
import hashlib

class Users(db.Model):
    __tablename__ = 'users'

    id  = db.Column(db.Integer, primary_key=True,autoincrement=True)
    
    email = db.Column(db.String(100),unique=True,nullable=False)
    password = db.Column(db.String(255),nullable=False)
    
    phone = db.Column(db.BigInteger,unique=True,nullable=False)
    cep = db.Column(db.BigInteger,nullable=False)
    address = db.Column(db.String(100),nullable=False)
    number_address = db.Column(db.BigInteger,nullable=True)
    
    complement = db.Column(db.String(255),nullable=False)
    district = db.Column(db.String(255),nullable=False)
    state = db.Column(db.String(10),nullable=False)
    city = db.Column(db.String(100),nullable=False)
    
    created_at = db.Column(db.DateTime,nullable=False,default=actualDate)
    is_admin = db.Column(db.Boolean,default=False)
    active = db.Column(db.Boolean,default=False)
    
    physical_id = db.Column(db.ForeignKey("physical_person.id",ondelete='cascade'),nullable=True)
    legal_id = db.Column(db.ForeignKey("legal_person.id",ondelete='cascade'),nullable=True)
    genre_id = db.Column(db.ForeignKey("genre_types.id",ondelete='cascade'),nullable=True)

    physical_ship = db.relationship('PhysicalPerson', back_populates="physical_children")
    legal_ship = db.relationship('LegalPerson', back_populates="legal_children")
    genre_ship = db.relationship('GenreTypes', back_populates="genre_children")
    
    user_order_children = db.relationship(
        "Orders", back_populates="user_ship",
        cascade="all, delete",passive_deletes=True)

    def __init__(self,email,password,phone,cep,address,number_address,
                 complement,district,city,state,genre_id=None,physical_id=None,legal_id=None,
                 is_admin=False,active=False,created_at=actualDate):

        self.password = hashlib.sha256(str.encode(password)).hexdigest()
        self.number_address= number_address
        self.created_at  = created_at()
        self.physical_id = physical_id
        self.complement = complement
        self.legal_id = legal_id
        self.genre_id = genre_id
        self.is_admin = is_admin
        self.district = district
        self.address = address
        self.active = active
        self.state = state
        self.email = email
        self.phone = phone
        self.city = city
        self.cep = cep


    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self,data):
        default= ['password']
        for key, value in data.items():
            if key in default:continue
            elif getattr(self,key,False):
                setattr(self, key, value)

        db.session.commit()
        return self