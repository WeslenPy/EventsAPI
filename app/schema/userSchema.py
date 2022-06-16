from app import ma
from app.models import Users

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Users
        load_instance = True
