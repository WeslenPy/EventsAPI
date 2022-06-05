from app import ma

class OperatorSchema(ma.Schema):
    class Meta:
        fields = ('id','name','symbol')

