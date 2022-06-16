from app import db

class Lots(db.Model):
    __tablename__ = 'lots'

    id  = db.Column(db.Integer, primary_key=True,autoincrement=True)
    
    quantity = db.Column(db.Integer,nullable=False)
    price = db.Column(db.Float(precision=2),nullable=False)
    
    start_date  = db.Column(db.DateTime,nullable=False)
    end_date  = db.Column(db.DateTime,nullable=False)
    
    status =  db.Column(db.Boolean,nullable=False)
    
    ticket_id = db.Column(db.ForeignKey("tickets.id",ondelete='cascade'),nullable=False)
    ticket_ship = db.relationship('Tickets', back_populates="ticket_children")
    
        
    lot_children = db.relationship(
        "Orders", back_populates="lot_ship",
        cascade="all, delete",passive_deletes=True)
    

    def __init__(self,quantity,price,start_date,end_date,ticket_id,status):

        self.quantity = quantity
        self.price = price
        self.start_date  =start_date
        self.end_date  =end_date
        self.ticket_id = ticket_id
        self.status = status
        

        
    def save(self):
        db.session.add(self)
        db.session.commit()