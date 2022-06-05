from app import ma

class ApiSchema(ma.Schema):
    class Meta:
        fields = ('id','api_name')

