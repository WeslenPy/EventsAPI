from app import db


class BlockingRule(db.Model):
    __tablename__ = 'blocking_rule'

    id  = db.Column(db.Integer, primary_key=True,autoincrement=True)

    interval = db.Column(db.Integer,nullable=False)
    cancellations_allowed = db.Column(db.Integer,nullable=False)
    blocking_time_minutes= db.Column(db.Integer,nullable=False)
    
    def __init__(self,interval,cancellations_allowed,blocking_time_minutes):
    
        self.interval = interval
        self.cancellations_allowed = cancellations_allowed
        self.blocking_time_minutes= blocking_time_minutes

