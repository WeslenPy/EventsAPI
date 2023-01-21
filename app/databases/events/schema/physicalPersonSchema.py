from app.server.instance import app

from app.databases.events.models    import PhysicalPerson

class PhysicalPersonSchema(app.ma.SQLAlchemyAutoSchema):
    class Meta:
        unknown = 'exclude'
        model = PhysicalPerson
        load_instance = True
        include_fk=True
        ordered = True
        dump_only = ("id",)