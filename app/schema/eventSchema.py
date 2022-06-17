from app import ma
from app.models import Events

class EventSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        unknown = "exclude"

        model = Events
        load_instance = True
