from app.server.instance import app
from app.databases.events.models import Orders,Users,Lots
from app.utils.functions.validitys import validity_field

from marshmallow import post_load,pre_load



class OrderSchema(app.ma.SQLAlchemyAutoSchema):

    @pre_load
    def check_ids(self,data,**kwargs):
        user_id = data.get('user_id',None)
        lot_id = data.get('lot_id',None)

        validity_field.find_field_model(Users,'id',user_id,'user_id')
        lot:Lots = validity_field.find_field_model(Lots,'id',lot_id,'lot_id')

        data['unit_price'] = lot.price
        data['final_price']= data['quantity'] * lot.price

        return data

    @post_load(pass_original=True)
    def _new(self,data,orignal_data,**kwargs):
        Orders(**orignal_data).save()
        return data

    class Meta:
        unknown = "exclude"
        model = Orders
        load_instance = True
        ordered = True
        include_fk=True
        dump_only = ("id",)
