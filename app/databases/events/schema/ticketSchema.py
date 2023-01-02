from app import ma
from app.database.models    import Tickets

class TicketSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        unknown = "exclude"
        include_fk=True
        ordered = True
        model = Tickets
        load_instance = True
        dump_only = ("id",)

