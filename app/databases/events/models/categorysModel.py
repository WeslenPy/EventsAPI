from app.server.instance import app
from datetime import datetime
import sqlalchemy

db:sqlalchemy = app.db

class Category(db.Model):
    __tablename__ = 'category'

    id  = db.Column(db.Integer, primary_key=True,autoincrement=True)
    
    name = db.Column(db.String(255),unique=True,nullable=False)
    description = db.Column(db.Text,nullable=True)
    status  =  db.Column(db.Boolean,nullable=False,default=True)
    created_at = db.Column(db.DateTime,nullable=False,default=datetime.now)
    
    category_children = db.relationship(
        "Events", back_populates="category_ship",
        cascade="all, delete",passive_deletes=True)
    

    def __init__(self,name,description='',status=True,created_at=datetime.now):

        self.description = description
        self.created_at = created_at()
        self.status = status
        self.name = name
        
    def __repr__(self) -> str:
        return self.name

    
    def save(self):
        db.session.add(self)
        db.session.commit()
        
