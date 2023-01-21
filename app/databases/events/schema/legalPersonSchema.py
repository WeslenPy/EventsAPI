from app.server.instance import app

from app.databases.events.models    import LegalPerson

class LegalPersonSchema(app.ma.SQLAlchemyAutoSchema):
    class Meta:
        unknown = "exclude"
        ordered = True
        model = LegalPerson
        include_fk=True
        load_instance = True
        dump_only = ("id",)
