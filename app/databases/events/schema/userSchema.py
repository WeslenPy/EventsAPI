from app.server.instance import app

from app.databases.events.models    import Users

from app.databases.events.schema.physicalPersonSchema import PhysicalPersonSchema
from app.databases.events.schema.legalPersonSchema import LegalPersonSchema
from app.databases.events.schema.genreTypesSchema import GenreTypeSchema
from app.databases.events.schema.termsEventSchema import TermsEventSchema
from app.databases.events.schema.userAccessTypesSchema import UserAccessTypesSchema

from app.utils.functions.validitys import validity_field,validity_cnpj,validity_cpf
from marshmallow import (ValidationError,
                        validates_schema,
                        validates,
                        pre_load,
                        post_load,)

class UserSchema(app.ma.SQLAlchemyAutoSchema):
    
    physical_ship = app.ma.Nested(PhysicalPersonSchema)
    legal_ship = app.ma.Nested(LegalPersonSchema)
    genre_ship = app.ma.Nested(GenreTypeSchema)
    
    types_children = app.ma.Nested(UserAccessTypesSchema,many=True)
    terms_children = app.ma.Nested(TermsEventSchema,many=True)

    email = app.ma.Email()

    @post_load(pass_original=True)
    def new_user(self,data,original_data,**kwargs):
        _schema = self.context.get('type',PhysicalPersonSchema)()
        try:result = _schema.load(original_data)
        except ValidationError as erro:
            raise ValidationError(erro.messages)

        field = self.context.get('field','physical_id')
        type_ = self.context.get('type_user',True)
        setattr(data, field,result.id)
        setattr(data, 'physical',type_)

        data.save()
        return data

    @validates_schema
    def unique(self,data,**kwargs):
        check = {"email":data['email'],'phone':data['phone']}
        cpf,cnpj = data.get('cpf',None), data.get('cnpj',None)
        if cpf:validity_cpf.validityCPF(cpf)
        if cnpj:validity_cnpj.validityCNPJ(cnpj)

        validity_field.unique(Users,check)
        return data

  
    
    class Meta:
        unknown = "exclude"
        model = Users

        load_instance = True
        include_fk=True
        ordered = True

        load_only = ("password",)
        dump_only = ("id",)

