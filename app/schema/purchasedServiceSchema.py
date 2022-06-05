from app import ma
        
class PurchasedSchema(ma.Schema):
    created_at = ma.DateTime(format='%d/%m H %H:%M:%S')
    class Meta:
        fields = ('id','price','status','service_number','ddi',
                        'url_image','name','created_at','user_id',
                        'service_id','activation_id','api_key','api_url')
