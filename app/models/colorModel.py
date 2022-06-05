from app import db


class Color(db.Model):
    __tablename__ = 'color'

    id  = db.Column(db.Integer, primary_key=True,autoincrement=True)

    name = db.Column(db.String(100),nullable=False)
    color_hex = db.Column(db.String(30),nullable=False,unique=True)

    color_name_ship = db.relationship('ServiceName',backref=db.backref('color', lazy=True))

    def __init__(self,name,color_hex):
    
        self.name = name
        self.color_hex = color_hex

    def __repr__(self) -> str:
        return self.name

