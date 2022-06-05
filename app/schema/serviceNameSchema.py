from app import ma

class ServiceNameSchema(ma.Schema):
    class Meta:
        fields = ('id','name','url_image','buy_price','color_hex')
        