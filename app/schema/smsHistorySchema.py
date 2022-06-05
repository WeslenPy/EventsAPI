from app import ma


class HistorySchema(ma.Schema):
    created_at = ma.DateTime(format='%d/%m H %H:%M:%S')
    received_at = ma.DateTime(format='%d/%m H %H:%M:%S')
    class Meta:
        fields = ('id','service_number','ddi','status','service_name_id',
                            'name','url_image','api_name','sms','received_at','created_at')


class HistoryCodeSchema(ma.Schema):
    received_at = ma.DateTime(format='%d/%m H %H:%M:%S')
    class Meta:
        fields = ('id','sms','received_at')

