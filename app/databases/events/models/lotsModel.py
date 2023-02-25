from app.utils.functions.date_fast import currentDate
from app.server.instance import app
import sqlalchemy


db:sqlalchemy = app.db

class Lots(db.Model):
    __tablename__ = 'lots'

    id  = db.Column(db.Integer, primary_key=True,autoincrement=True)
    
    quantity = db.Column(db.Integer,nullable=False)
    price = db.Column(db.Float(precision=2),nullable=False)
    
    start_date  = db.Column(db.DateTime,nullable=False)
    end_date  = db.Column(db.DateTime,nullable=False)
    created_at = db.Column(db.DateTime,nullable=False,default=currentDate)
    
    status  = db.Column(db.Boolean,nullable=False,default=True)
    closed  = db.Column(db.Boolean,nullable=False,default=False)
    
    ticket_id = db.Column(db.ForeignKey("tickets.id",ondelete='cascade'),nullable=False)
    user_id = db.Column(db.ForeignKey("users.id",ondelete='cascade'),nullable=False)

    ticket_ship = db.relationship('Tickets', back_populates="lot_children")
    user_ship = db.relationship('Users', back_populates="lot_children")
        
    lot_children = db.relationship(
        "Orders", back_populates="lot_ship",
        cascade="all, delete",passive_deletes=True)
    

    def __init__(self,quantity,ticket_id,price,start_date,end_date,
                                status=True,closed=False,created_at=currentDate):

        
        self.price = price
        self.status = status
        self.closed = closed
        self.end_date = end_date
        self.quantity = quantity
        self.ticket_id = ticket_id
        self.start_date = start_date
        self.created_at = created_at()
        

        
    def save(self):
        db.session.add(self)
        db.session.commit()