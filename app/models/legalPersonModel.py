from app import db

class LegalPerson(db.Model):
    __tablename__ = 'legal_person'

    id  = db.Column(db.Integer, primary_key=True,autoincrement=True)
    
    corporate_name = db.Column(db.String(255),unique=True,nullable=False)
    cnpj = db.Column(db.String(20),nullable=False,unique=True)
    
    legal_children = db.relationship(
        "Users", back_populates="legal_ship",
        cascade="all, delete",passive_deletes=True) 

    def __init__(self,corporate_name,cnpj):

        self.corporate_name = corporate_name
        self.cnpj = cnpj
        
    def __repr__(self) -> str:
        return self.corporate_name
        
    def save(self):
        db.session.add(self)
        db.session.commit()