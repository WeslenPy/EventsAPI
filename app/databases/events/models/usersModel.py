from .userTypeAccessModel import UserAccessTypes
from .userTypesModel import UserTypes

from app.utils.functions.date_fast import currentDate
from app.utils.functions.encrypt_password import encryptPassword
from app.server.instance import app
import sqlalchemy

db:sqlalchemy = app.db
class Users(db.Model):
    __tablename__ = 'users'

    id  = db.Column(db.Integer, primary_key=True,autoincrement=True)
    
    email = db.Column(db.String(100),unique=True,nullable=False)
    password = db.Column(db.String(255),nullable=False)
    
    phone = db.Column(db.String(15),unique=True,nullable=False)
    zip_code = db.Column(db.String(8),nullable=False)
    address = db.Column(db.String(100),nullable=False)
    number_address = db.Column(db.BigInteger,nullable=False)
    
    complement = db.Column(db.String(255),nullable=False)
    district = db.Column(db.String(255),nullable=False)
    state = db.Column(db.String(2),nullable=False)
    city = db.Column(db.String(100),nullable=False)
    
    created_at = db.Column(db.DateTime,nullable=False,default=currentDate)
    active = db.Column(db.Boolean,default=False)
    physical = db.Column(db.Boolean,default=False)
    
    physical_id = db.Column(db.ForeignKey("physical_person.id",ondelete='cascade'),nullable=True)
    legal_id = db.Column(db.ForeignKey("legal_person.id",ondelete='cascade'),nullable=True)

    physical_ship = db.relationship('PhysicalPerson', back_populates="physical_children")
    legal_ship = db.relationship('LegalPerson', back_populates="legal_children")
    
    user_order_children = db.relationship(
        "Orders", back_populates="user_ship",
        cascade="all, delete",passive_deletes=True)    
        
    user_event_children = db.relationship(
        "Events", back_populates="user_ship",
        cascade="all, delete",passive_deletes=True)  
        
    user_partner_children = db.relationship(
        "Partner", back_populates="user_ship",
        cascade="all, delete",passive_deletes=True)   
        
    user_tickets_children = db.relationship(
        "Tickets", back_populates="user_ticket_ship",
        cascade="all, delete",passive_deletes=True)

    rules_user_children = db.relationship(
        "RulesEvent", back_populates="user_ship",
        cascade="all, delete",passive_deletes=True)   
        
    terms_children = db.relationship(
        "TermsEvent", back_populates="user_ship",
        cascade="all, delete",passive_deletes=True)

    types_children = db.relationship(
        "UserAccessTypes", back_populates="user_ship",
        cascade="all, delete",passive_deletes=True) 
    
   

    def __init__(self,email,password,phone,zip_code,address,number_address,
                 complement,district,city,state,physical=True,
                physical_id=None,legal_id=None,
                 is_admin=False,active=False,created_at=currentDate):

        self.password = encryptPassword(password)
        self.number_address= number_address
        self.created_at  = created_at()
        self.physical_id = physical_id
        self.physical = physical
        self.complement = complement
        self.legal_id = legal_id
        self.is_admin = is_admin
        self.district = district
        self.address = address
        self.active = active
        self.state = state
        self.email = email.strip().lower()
        self.phone = phone
        self.city = city
        self.zip_code = zip_code

    
    def default_add(self):
        type_:UserTypes = UserTypes.query.filter_by(type='user',status=True).first()
        if type_:
            new:UserAccessTypes  = UserAccessTypes(user_id=self.id,type_id=type_.id)
            new.save()

    def save(self):
        db.session.add(self)
        db.session.commit()
        self.default_add()

    def update(self,data:dict):
        default= ['password','id']
        for key, value in data.items():
            if key in default:continue
            elif getattr(self,key,"not data") != "not data":
                setattr(self, key, value)

        db.session.commit()
        return self