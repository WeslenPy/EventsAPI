from app.utils.functions.date_fast import currentDate
from app.server.instance import app
import sqlalchemy


db:sqlalchemy = app.db

class Tickets(db.Model):
    __tablename__ = 'tickets'

    id  = db.Column(db.Integer, primary_key=True,autoincrement=True)
    
    title = db.Column(db.String(255),nullable=False)
    description = db.Column(db.Text,nullable=True)
    max_buy =  db.Column(db.BigInteger,nullable=False)
    min_buy =  db.Column(db.BigInteger,nullable=False)
    price = db.Column(db.Float(precision=2),nullable=False)
    paid = db.Column(db.Boolean,nullable=False)
    status =  db.Column(db.Boolean,nullable=False,default=True)

    created_at = db.Column(db.DateTime,nullable=False,default=currentDate)

    user_id = db.Column(db.ForeignKey("users.id",ondelete='cascade'),nullable=False)
    
    user_ticket_ship = db.relationship('Users', back_populates="user_tickets_children")
    
    lot_children = db.relationship(
        "Lots", back_populates="ticket_ship",
        cascade="all, delete",passive_deletes=True)
      
    ticket_event_children = db.relationship(
        "Events", back_populates="ticket_ship",
        cascade="all, delete",passive_deletes=True)
    
    def __init__(self,title,max_buy,min_buy,paid,user_id,price,description='',
                        status=True,created_at=currentDate):

        self.description = description
        self.created_at = created_at()
        self.max_buy = max_buy
        self.min_buy = min_buy
        self.user_id = user_id
        self.status = status
        self.price = price
        self.title = title
        self.paid = paid
        
    def __repr__(self) -> str:
        return self.title
        
        
    def save(self):
        db.session.add(self)
        db.session.commit()