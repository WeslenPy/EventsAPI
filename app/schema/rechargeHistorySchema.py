from app import ma

class HistoryPaymentSchema(ma.Schema):
    created_at = ma.DateTime(format='%d/%m H %H:%M:%S')
    class Meta:
        fields = ('id','created_at','expiration','status','value','method','url')
