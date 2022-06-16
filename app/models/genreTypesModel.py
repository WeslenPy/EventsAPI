from app.utils.functions.date_fast import actualDate
from app import db

class GenreTypes(db.Model):
    __tablename__ = 'genre_types'

    id  = db.Column(db.Integer, primary_key=True,autoincrement=True)
    
    type = db.Column(db.String(30),unique=True,nullable=False)
    description = db.Column(db.Text,nullable=True)

    created_at = db.Column(db.DateTime,nullable=False,default=actualDate)
    status = db.Column(db.Boolean,default=True)
    
    genre_children = db.relationship(
        "Users", back_populates="genre_ship",
        cascade="all, delete",passive_deletes=True) 

    def __init__(self,type,description,status=True,created_at=actualDate):

        self.type = type
        self.status = status
        self.description = description
        self.created_at  = created_at()
        
    def __repr__(self) -> str:
        return self.type

    
    def save(self):
        db.session.add(self)
        db.session.commit()
        
