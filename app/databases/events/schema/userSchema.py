from app.server.instance import app

from app.databases.events.models    import Users

from app.databases.events.schema.physicalPersonSchema import PhysicalPersonSchema
from app.databases.events.schema.legalPersonSchema import LegalPersonSchema
from app.databases.events.schema.genreTypesSchema import GenreTypeSchema
from app.databases.events.schema.termsEventSchema import TermsEventSchema
from app.databases.events.schema.userAccessTypesSchema import UserAccessTypesSchema

from flask import request,render_template
from flask_mail import Message

from app.utils.functions.validitys import validity_field,validity_cnpj,validity_cpf
from marshmallow import (ValidationError,
                        validates_schema,
                        validates,
                        pre_dump,
                        post_load,)

class UserSchema(app.ma.SQLAlchemyAutoSchema):
    
    physical_ship = app.ma.Nested(PhysicalPersonSchema)
    legal_ship = app.ma.Nested(LegalPersonSchema)
    
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

        if app.app.config.get("ENABLED_EMAIL",False):
            token_url = app.tokenSafe.dumps(data.email,salt=app.app.config["TOKEN_SALT"])
            msg = Message("Não responda este e-mail",
                    sender=app.app.config['MAIL_USERNAME'],
                    recipients=[data.email])

            url_root = request.base_url.replace(request.path,f'/confirm/{token_url}')

            name:str = result.full_name if getattr(result,"full_name",None) !=None else getattr(result,"corporate_name",None)
            
            msg.html = str(render_template('email/confirm_email.html',url_validity=url_root,username=name.split(' ')[0].capitalize()))
            app.executor.submit(app.mail.send,msg)

        else:data.active=True

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

