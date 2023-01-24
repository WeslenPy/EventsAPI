from app.server.instance import app

from app.databases.events.models    import Tickets,Users
from app.utils.functions.validitys import validity_field
from marshmallow import post_load,validates
class TicketSchema(app.ma.SQLAlchemyAutoSchema):

    @post_load
    def new_ticket(self,data,**kwargs):
        data.save()
        return data

    @validates('user_id')
    def check_user_id(self,data,**kwargs):
        validity_field.find_field_model(Users,'id',data,'user_id')
        return data

    class Meta:
        unknown = "exclude"
        include_fk=True
        ordered = True
        model = Tickets
        load_instance = True
        dump_only = ("id",)

