from app.utils.functions.date_fast import currentDate
from app import db

class UserAccessTypes(db.Model):
    __tablename__ = 'user_access_types'

    id  = db.Column(db.Integer, primary_key=True,autoincrement=True)
    
    user_id = db.Column(db.ForeignKey("users.id",ondelete='cascade'),nullable=False)
    type_id = db.Column(db.ForeignKey("user_types.id",ondelete='cascade'),nullable=False)
    
    type_ship = db.relationship('UserTypes', back_populates="user_types_children")
    user_ship = db.relationship('Users', back_populates="types_children")

    created_at = db.Column(db.DateTime,nullable=False,default=currentDate)
    status = db.Column(db.Boolean,default=True)
    

    def __init__(self,user_id,type_id,status=True,created_at=currentDate):

        self.type_id = type_id
        self.user_id = user_id
        self.status = status
        self.created_at  = created_at()
        
    def __repr__(self) -> str:
        return str(self.type_ship.type)

    def save(self):
        db.session.add(self)
        db.session.commit()
        
