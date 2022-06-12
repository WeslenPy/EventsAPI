from app.utils.functions.date_fast import actualDate
from app import db

class Orders(db.Model):
    __tablename__ = 'orders'

    id  = db.Column(db.Integer, primary_key=True,autoincrement=True)
    
    method = db.Column(db.String(50),nullable=False)
    value = db.Column(db.Float(precision=2),nullable=False)
    
    created_at = db.Column(db.DateTime,nullable=False,default=actualDate)
    payment_at = db.Column(db.DateTime,nullable=True)
    
    status  = db.Column(db.String(50),nullable=False)

    lot_id = db.Column(db.ForeignKey("lots.id",ondelete='cascade'),nullable=False)
    user_id = db.Column(db.ForeignKey("users.id",ondelete='cascade'),nullable=False)
    
    lot_ship = db.relationship('Lots', back_populates="lot_children")    
    user_ship = db.relationship('Users', back_populates="user_order_children")
    
    
    def __init__(self,method,value,status,payment_at,lot_id,user_id,created_at=actualDate):

        self.method = method
        self.value = value
        self.status  =status
        self.lot_id  =lot_id
        self.user_id  =user_id
        self.payment_at  =payment_at
        self.created_at  =created_at()
        
