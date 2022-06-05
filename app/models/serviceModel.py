from app import db

class Service(db.Model):
    __tablename__ = 'service'

    id  = db.Column(db.Integer, primary_key=True,autoincrement=True)

    amount = db.Column(db.Integer,nullable=False)

    sell_price = db.Column(db.Float(precision=2),nullable=False)

    api_id = db.Column(db.Integer,db.ForeignKey("api.id"),nullable=False)
    country_id = db.Column(db.Integer,db.ForeignKey("country.id"),nullable=False)
    service_name_id = db.Column(db.Integer,db.ForeignKey("service_name.id"),nullable=False)

    purchased_service_ship = db.relationship('PurchasedService',backref=db.backref('service', lazy=True))
    
    status = db.Column(db.Boolean,nullable=False)

    def __init__(self,status,amount,sell_price,api_id,country_id,service_name_id):
    
        self.sell_price= sell_price
        self.amount= amount
        self.service_name_id = service_name_id
        self.api_id= api_id
        self.country_id= country_id
        self.status = status

    def __repr__(self) -> str:
        return str(self.id)

