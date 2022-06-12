from app import db

class Category(db.Model):
    __tablename__ = 'category'

    id  = db.Column(db.Integer, primary_key=True,autoincrement=True)
    
    name = db.Column(db.String(255),unique=True,nullable=False)
    description = db.Column(db.Text,nullable=True)
    status  =  db.Column(db.Boolean,nullable=False)
    
    category_children = db.relationship(
        "Events", back_populates="category_ship",
        cascade="all, delete",passive_deletes=True)
    

    def __init__(self,name,description,status=True):

        self.description = description
        self.status = status
        self.name = name
        
    def __repr__(self) -> str:
        return self.name
        
