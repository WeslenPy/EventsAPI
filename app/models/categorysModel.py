from app import db

class Category(db.Model):
    __tablename__ = 'category'

    id  = db.Column(db.Integer, primary_key=True,autoincrement=True)
    
    name = db.Column(db.String(255),unique=True,nullable=False)
    description = db.Column(db.Text,nullable=True)

    def __init__(self,name,description):

        self.description = description
        self.name = name
        
    def __repr__(self) -> str:
        return self.name
        
