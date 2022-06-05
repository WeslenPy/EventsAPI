from app import db

class API(db.Model):
    __tablename__ = 'api'

    id  = db.Column(db.Integer, primary_key=True,autoincrement=True)

    api_name = db.Column(db.String(60),nullable=False,unique=True)
    api_url = db.Column(db.String(255),nullable=False)
    api_key = db.Column(db.String(255),nullable=False,unique=True)
    obs = db.Column(db.Text,nullable=True)
    by_sms = db.Column(db.Boolean,default=False)
    
    service_api_ship = db.relationship('Service',backref=db.backref('api', lazy=True))
    purchased_api_ship = db.relationship('PurchasedService',backref=db.backref('api', lazy=True))
    
    
    def __init__(self,api_name,api_url,api_key,obs,by_sms=False):
    
        self.api_name = api_name
        self.api_url = api_url
        self.api_key= api_key
        self.by_sms= by_sms
        self.obs= obs

    def __repr__(self) -> str:
        return self.api_name
        


