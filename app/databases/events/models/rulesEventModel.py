from app.utils.functions.date_fast import currentDate
from app import db

class RulesEvent(db.Model):
    __tablename__ = 'rules_events'

    id  = db.Column(db.Integer, primary_key=True,autoincrement=True)
    
    type = db.Column(db.String(255),nullable=False)
    description = db.Column(db.Text,nullable=True)

    created_at = db.Column(db.DateTime,nullable=False,default=currentDate)
    status = db.Column(db.Boolean,default=True)
    
    user_id = db.Column(db.ForeignKey("users.id",ondelete='cascade'),nullable=False)
    event_id = db.Column(db.ForeignKey("events.id",ondelete='cascade'),nullable=False)

    event_ship = db.relationship('Events', back_populates="rules_event_children")
    user_ship = db.relationship('Users', back_populates="rules_user_children")

    def __init__(self,type,description,event_id,user_id,status=True,created_at=currentDate):

        self.type = type
        self.status = status
        self.user_id = user_id
        self.event_id = event_id
        self.description = description
        self.created_at  = created_at()
        
    def __repr__(self) -> str:
        return self.type

    
    def save(self):
        db.session.add(self)
        db.session.commit()
        
