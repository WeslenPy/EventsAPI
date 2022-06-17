from app import ma
from app.models import Users

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        unknown = "exclude"

        model = Users
        load_instance = True
