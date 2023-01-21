from app.server.instance import app

from app.databases.events.models    import Tickets

class TicketSchema(app.ma.SQLAlchemyAutoSchema):

    class Meta:
        unknown = "exclude"
        include_fk=True
        ordered = True
        model = Tickets
        load_instance = True
        dump_only = ("id",)

