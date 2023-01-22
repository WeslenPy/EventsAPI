from app.utils.functions.date_fast import currentDate
from app.server.instance import app
import sqlalchemy


db:sqlalchemy = app.db

class Orders(db.Model):
    __tablename__ = 'orders'

    id  = db.Column(db.Integer, primary_key=True,autoincrement=True)
    
    method = db.Column(db.String(50),nullable=True)
    value = db.Column(db.Float(precision=2),nullable=False)
    quantity = db.Column(db.Integer,nullable=False)
    
    created_at = db.Column(db.DateTime,nullable=False,default=currentDate)
    payment_at = db.Column(db.DateTime,nullable=True)
    expired_at = db.Column(db.DateTime,nullable=False,default=currentDate)
    
    status  = db.Column(db.Enum('Pending','Approved','Expired'),nullable=False,default='Pending')

    lot_id = db.Column(db.ForeignKey("lots.id",ondelete='cascade'),nullable=False)
    user_id = db.Column(db.ForeignKey("users.id",ondelete='cascade'),nullable=False)
    
    lot_ship = db.relationship('Lots', back_populates="lot_children")    
    user_ship = db.relationship('Users', back_populates="user_order_children")
    
    def __init__(self,value,lot_id,user_id,quantity,method='',expired_at=currentDate,
                            status='Pending',payment_at=None,created_at=currentDate):

        self.method = method
        self.value = value
        self.quantity = quantity
        self.status  =status
        self.lot_id  =lot_id
        self.user_id  =user_id
        self.expired_at = expired_at()
        self.payment_at = payment_at
        self.created_at = created_at()
        
    def save(self):
        db.session.add(self)
        db.session.commit()