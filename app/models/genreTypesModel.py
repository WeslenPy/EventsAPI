from app.utils.functions.date_fast import actualDate
from app import db

class GenreTypes(db.Model):
    __tablename__ = 'genre_types'

    id  = db.Column(db.Integer, primary_key=True,autoincrement=True)
    
    type = db.Column(db.String(30),unique=True,nullable=False)
    description = db.Column(db.Text,nullable=True)

    created_at = db.Column(db.DateTime,nullable=False,default=actualDate)
    active = db.Column(db.Boolean,default=True)

    def __init__(self,type,description,active=True,created_at=actualDate):

        self.type = type
        self.active = active
        self.description = description
        self.created_at  = created_at()
        
    def __repr__(self) -> str:
        return self.type
        
