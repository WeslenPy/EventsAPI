from app.server.instance import app

from app.databases.events.models    import LegalPerson
from marshmallow import post_load,validates_schema
from app.utils.functions.validitys import validity_field

class LegalPersonSchema(app.ma.SQLAlchemyAutoSchema):

    @validates_schema
    def unique_input(self,data,**kwargs):
        check = {'cnpj':data.get('cnpj',None)}
        validity_field.unique(LegalPerson,check)
        return data
    
    @post_load(pass_original=True)
    def _new_user(self,data,orignal_data,**kwargs):
        LegalPerson(**orignal_data).save()
        return data

    class Meta:
        unknown = 'exclude'
        model = LegalPerson
        load_instance = True
        include_fk=True
        ordered = True
        dump_only = ("id",)