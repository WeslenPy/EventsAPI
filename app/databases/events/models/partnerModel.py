from app.utils.functions.date_fast import currentDate
from app.server.instance import app
import sqlalchemy


db:sqlalchemy = app.db


class Partner(db.Model):
    __tablename__ = 'partner'

    id  = db.Column(db.Integer, primary_key=True,autoincrement=True)
    
    created_at  = db.Column(db.DateTime,nullable=False,default=currentDate)
    
    status =  db.Column(db.Boolean,nullable=False,default=True)
    
    user_id = db.Column(db.ForeignKey("users.id",ondelete='cascade'),nullable=False)
    user_ship = db.relationship('Users', back_populates="user_partner_children")
            
    event_id = db.Column(db.ForeignKey("events.id",ondelete='cascade'),nullable=False)
    event_ship = db.relationship('Events', back_populates="event_partner_children")
        
    def __init__(self,user_id,event_id,created_at=currentDate,status=True):

        self.user_id = user_id
        self.event_id = event_id
        self.created_at  =created_at()
        self.status = status
        
    def save(self):
        db.session.add(self)
        db.session.commit()