from app import db


class Country(db.Model):
    __tablename__ = 'country'

    id  = db.Column(db.Integer, primary_key=True,autoincrement=True)

    country_name = db.Column(db.String(100),nullable=False,unique=True)
    number_country = db.Column(db.Integer,nullable=False,unique=True)
    flag = db.Column(db.String(100),nullable=True)
    ddi = db.Column(db.Integer,nullable=False)

    service_country_ship = db.relationship('Service',backref=db.backref('country', lazy=True))

    def __init__(self,country_name,number_country,ddi,flag=False):
    
        self.country_name = country_name
        self.number_country= number_country
        self.flag = flag
        self.ddi = ddi

    def __repr__(self) -> str:
        return self.country_name
