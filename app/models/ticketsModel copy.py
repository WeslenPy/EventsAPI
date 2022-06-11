from app import db

class Tickets(db.Model):
    __tablename__ = 'tickets'

    id  = db.Column(db.Integer, primary_key=True,autoincrement=True)
    
    title = db.Column(db.String(255),nullable=False)
    description = db.Column(db.Text,nullable=False)

    def __init__(self,name,description):

        self.description = description
        self.name = name
        
    def __repr__(self) -> str:
        return self.name
        
