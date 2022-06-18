from app.utils.functions.date_fast import actualDate
from app import db

class Tickets(db.Model):
    __tablename__ = 'tickets'

    id  = db.Column(db.Integer, primary_key=True,autoincrement=True)
    
    title = db.Column(db.String(255),nullable=False)
    description = db.Column(db.Text,nullable=False)
    max_buy =  db.Column(db.BigInteger,nullable=False)
    min_buy =  db.Column(db.BigInteger,nullable=False)
    paid = db.Column(db.Boolean,nullable=False)

    created_at = db.Column(db.DateTime,nullable=False,default=actualDate)
    
    ticket_lot_children = db.relationship(
        "Lots", back_populates="ticket_ship",
        cascade="all, delete",passive_deletes=True)
      
    ticket_event_children = db.relationship(
        "Events", back_populates="ticket_ship",
        cascade="all, delete",passive_deletes=True)
    
    def __init__(self,title,description,max_buy,min_buy,paid,created_at=actualDate):

        self.description = description
        self.created_at = created_at()
        self.max_buy = max_buy
        self.min_buy = min_buy
        self.title = title
        self.paid = paid
        
    def __repr__(self) -> str:
        return self.title
        
        
    def save(self):
        db.session.add(self)
        db.session.commit()