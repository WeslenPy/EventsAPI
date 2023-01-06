from app.utils.functions.date_fast import actualDate
from app import db

class TermsEvent(db.Model):
    __tablename__ = 'terms_event'

    id  = db.Column(db.Integer, primary_key=True,autoincrement=True)
    type_term = db.Column(db.String(100),nullable=False)
    description = db.Column(db.Text,nullable=False)
    
    term = db.Column(db.String(255),nullable=False)
    status  = db.Column(db.Boolean,nullable=False,default=True)
    created_at  = db.Column(db.DateTime,nullable=False,default=actualDate)

    event_id = db.Column(db.ForeignKey("events.id",ondelete='cascade'),nullable=False)
    user_id = db.Column(db.ForeignKey("users.id",ondelete='cascade'),nullable=False)
    
    event_ship = db.relationship('Events', back_populates="terms_children")
    user_ship = db.relationship('Users', back_populates="terms_children")
    

    def __init__(self,type_term,description,term,event_id,user_id,
                                status=True,created_at=actualDate):

        self.type_term = type_term
        self.user_id = user_id
        self.status = status
        self.description = description
        self.term = term
        self.event_id = event_id
        self.created_at = created_at()
        
    def save(self):
        db.session.add(self)
        db.session.commit()