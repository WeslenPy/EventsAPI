from app.utils.functions.validitys import validity_field
from app.databases.events.models import TermsEvent,Events,Users
from marshmallow import validates,pre_load,post_load
from app.server.instance import app

from app.utils.functions import aws
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
class TermsEventSchema(app.ma.SQLAlchemyAutoSchema):

    @post_load(pass_original=True)
    def _new(self,data,original_data,**kwargs):
        TermsEvent(**original_data).save()
        return data

    @pre_load
    def upload_files(self,data,**kwargs):
        term:FileStorage =  data.get('term_file',None)

        if term:data['url'] = aws.upload_file(term,secure_filename(term.filename))

        return data

    @validates('event_id')
    def exists_event_id(self,data,**kwargs):
        validity_field.find_field_model(Events,'id',data,'event_id')
        return data    
    
    @validates('user_id')
    def exists_user_id(self,data,**kwargs):
        validity_field.find_field_model(Users,'id',data,'user_id')
        return data
        
    class Meta:
        unknown = "exclude"
        ordered = True
        model = TermsEvent
        load_instance = True
        dump_only = ("id",)
