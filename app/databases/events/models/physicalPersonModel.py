from app.server.instance import app
db = app.db

class PhysicalPerson(db.Model):
    __tablename__ = 'physical_person'

    id  = db.Column(db.Integer, primary_key=True,autoincrement=True)
    
    full_name = db.Column(db.String(255),nullable=False)
    cpf = db.Column(db.String(20),nullable=False,unique=True)
    birth_date =  db.Column(db.DateTime,nullable=False)
    
    physical_children = db.relationship(
        "Users", back_populates="physical_ship",
        cascade="all, delete",passive_deletes=True) 

    def __init__(self,full_name,cpf,birth_date):

        self.birth_date = birth_date
        self.full_name = full_name
        self.cpf = cpf
        
    def __repr__(self) -> str:
        return self.full_name

    
    def update(self,data:dict):
        default= ['id',"cpf"]
        for key, value in data.items():
            if key in default:continue
            elif getattr(self,key,False):
                setattr(self, key, value)

        db.session.commit()
        return self
        
    def save(self):
        db.session.add(self)
        db.session.commit()