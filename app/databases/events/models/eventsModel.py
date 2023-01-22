from app.utils.functions.date_fast import currentDate
from app.server.instance import app

import sqlalchemy


db:sqlalchemy = app.db
class Events(db.Model):
    __tablename__ = 'events'

    id  = db.Column(db.Integer, primary_key=True,autoincrement=True)

    name = db.Column(db.String(255),nullable=False)
    locale_name = db.Column(db.String(256),nullable=False)
    image = db.Column(db.String(255),nullable=False)
    video = db.Column(db.String(255),nullable=False)
    
    cep = db.Column(db.String(25),nullable=False)
    state = db.Column(db.String(30),nullable=False)
    address = db.Column(db.String(255),nullable=False)
    number_address = db.Column(db.BigInteger,nullable=True)
    
    complement = db.Column(db.String(255),nullable=False)
    district = db.Column(db.String(100),nullable=False)
    city = db.Column(db.String(100),nullable=False)
    
    start_hour = db.Column(db.DateTime,nullable=False)
    start_date = db.Column(db.DateTime,nullable=False)
    end_date = db.Column(db.DateTime,nullable=False)
    created_at = db.Column(db.DateTime,nullable=False,default=currentDate)
    
    status = db.Column(db.Boolean,default=False)
    
    category_id = db.Column(db.ForeignKey("category.id",ondelete='cascade'),nullable=False)
    ticket_id = db.Column(db.ForeignKey("tickets.id",ondelete='cascade'),nullable=False)
    user_id = db.Column(db.ForeignKey("users.id",ondelete='cascade'),nullable=False)
    
    category_ship = db.relationship('Category', back_populates="category_children")
    ticket_ship = db.relationship('Tickets', back_populates="ticket_event_children")
    user_ship = db.relationship('Users', back_populates="user_event_children")


    event_partner_children = db.relationship(
        "Partner", back_populates="event_ship",
        cascade="all, delete",passive_deletes=True)

    rules_event_children = db.relationship(
        "RulesEvent", back_populates="event_ship",
        cascade="all, delete",passive_deletes=True)
        
    terms_children = db.relationship(
        "TermsEvent", back_populates="event_ship",
        cascade="all, delete",passive_deletes=True)


    def __init__(self,name,image,video,cep,address,number_address,state,
                 complement,district,city,start_hour,start_date,end_date,category_id,
                 ticket_id,user_id,locale_name,status=False,created_at=currentDate):

        self.number_address= number_address
        self.created_at  = created_at()
        self.category_id = category_id
        self.locale_name = locale_name
        self.ticket_id = ticket_id
        self.complement = complement
        self.start_date = start_date
        self.start_hour = start_hour
        self.end_date = end_date
        self.district = district
        self.address = address
        self.user_id = user_id
        self.status = status
        self.image = image
        self.video = video
        self.state = state
        self.name = name
        self.city = city
        self.cep = cep
    
    def __repr__(self) -> str:
        return self.name

    def save(self):
        db.session.add(self)
        db.session.commit()
        
