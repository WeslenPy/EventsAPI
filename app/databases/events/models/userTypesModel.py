from app.utils.functions.date_fast import currentDate
from app import db

class UserTypes(db.Model):
    __tablename__ = 'user_types'

    id  = db.Column(db.Integer, primary_key=True,autoincrement=True)
    
    type = db.Column(db.String(30),unique=True,nullable=False)
    access_level = db.Column(db.Integer,nullable=False,default=0)
    description = db.Column(db.Text,nullable=True)

    created_at = db.Column(db.DateTime,nullable=False,default=currentDate)
    status = db.Column(db.Boolean,default=True)
    
    user_types_children = db.relationship(
        "UserAccessTypes", back_populates="type_ship",
        cascade="all, delete",passive_deletes=True) 

    def __init__(self,type,description,access_level=0,status=True,created_at=currentDate):

        self.type = type
        self.status = status
        self.description = description
        self.created_at  = created_at()
        self.access_level = access_level
        
    def __repr__(self) -> str:
        return self.type

    
    def save(self):
        db.session.add(self)
        db.session.commit()
        
