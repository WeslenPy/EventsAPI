from app import db

class Lots(db.Model):
    __tablename__ = 'lots'

    id  = db.Column(db.Integer, primary_key=True,autoincrement=True)
    
    quantity = db.Column(db.Integer,nullable=False)
    price = db.Column(db.Float(precision=2),nullable=False)
    
    start_date  = db.Column(db.DateTime,nullable=False)
    end_date  = db.Column(db.DateTime,nullable=False)

    def __init__(self,quantity,price,start_date,end_date):

        self.quantity = quantity
        self.price = price
        self.start_date  =start_date
        self.end_date  =end_date
        
