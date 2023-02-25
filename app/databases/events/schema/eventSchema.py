from app.server.instance import app

from app.databases.events.models    import Events,Tickets,Category,Users

from app.databases.events.schema.categorySchema import CategorySchema
from app.databases.events.schema.ticketSchema import TicketSchema
from app.databases.events.schema.userSchema import UserSchema
from app.databases.events.schema.partnerSchema import PartnerUserSchema
from app.databases.events.schema.rulesEventSchema import RulesEventSchema
from app.databases.events.schema.termsEventSchema import TermsEventSchema

from marshmallow import pre_load,post_load,fields,validates_schema
from app.utils.functions.validitys import validity_field

from app.utils.functions import aws
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage


class DateTimeIso(fields.Field):
    def _serialize(self, value, attr, obj,**kwargs):
        if value is None:return None
        return obj.datetime_isoformat(value)

class EventSchema(app.ma.SQLAlchemyAutoSchema):
    
    event_partner_children = app.ma.Nested(PartnerUserSchema,many=True)
    terms_children = app.ma.Nested(TermsEventSchema,many=True)
    rules_event_children = app.ma.Nested(RulesEventSchema,many=True)
    ticket_ship = app.ma.Nested(TicketSchema)
    category_ship = app.ma.Nested(CategorySchema)
    user_ship = app.ma.Nested(UserSchema)

    image = app.ma.String(required=True)
    video = app.ma.String(required=True)

    start_date = DateTimeIso(required=True)
    start_hour = DateTimeIso(required=True)
    end_date = DateTimeIso(required=True)
    
    @validates_schema
    def validates_fields(self,data,**kwargs):
        category_id = data.get('category_id',None)
        ticket_id = data.get('ticket_id',None)
        user_id = data.get('user_id',None)

        validity_field.find_field_model(Users,{'id':user_id,"active":True},'user_id')
        validity_field.find_field_model(Category,{'id':category_id,"status":True},'category_id')
        validity_field.find_field_model(Tickets,{'id':ticket_id,'user_id':user_id,"status":True},'ticket_id')

        return data



    @pre_load
    def upload_files(self,data,**kwargs):
        video:FileStorage  = data.get('video',None)
        image:FileStorage =  data.get('image',None)

        if video:data['video'] = aws.upload_file(video,secure_filename(video.filename))
        if image:data['image'] = aws.upload_file(image,secure_filename(image.filename))

        return data

    @post_load(pass_original=True)
    def _new(self,data,original_data,**kwargs):
        Events(**original_data).save()
        return data
    



    class Meta:
        model = Events
        ordered = True
        include_fk=True
        load_instance = True
        # unknown = "exclude"
        dump_only = ("id",)

