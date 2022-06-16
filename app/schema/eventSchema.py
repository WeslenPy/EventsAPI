from app import ma
from app.models import Events

class EventSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Events
        load_instance = True
