from app import db


class ServiceName(db.Model):
    __tablename__ = 'service_name'

    id  = db.Column(db.Integer, primary_key=True,autoincrement=True)

    name = db.Column(db.String(50),nullable=False,unique=True)
    url_image = db.Column(db.String(255),nullable=False)
    buy_price = db.Column(db.Float(precision=2),nullable=False)
    symbol = db.Column(db.String(5),nullable=False)
    more_buy = db.Column(db.BigInteger,nullable=False,default=0)

    color_id = db.Column(db.Integer,db.ForeignKey("color.id"),nullable=False)

    service_ship = db.relationship('Service',backref=db.backref('service_name', lazy=True))
    
    def __init__(self,name,color_id,symbol,buy_price,url_image):

        self.name = name
        self.color_id = color_id
        self.url_image = url_image
        self.symbol = symbol
        self.buy_price = buy_price
        
    def __repr__(self) -> str:
        return self.name