from app import db


class Operator(db.Model):
    __tablename__ = 'operator'

    id  = db.Column(db.Integer, primary_key=True,autoincrement=True)

    name = db.Column(db.String(20),nullable=False)
    symbol = db.Column(db.String(20), unique=True,nullable=False)

    operator_purchased_ship = db.relationship('PurchasedService',
                                         backref=db.backref('operator', lazy=True))
    

    def __init__(self,name,symbol) -> None:
        self.symbol = symbol
        self.name = name

    def __repr__(self) -> str:
        return self.name

