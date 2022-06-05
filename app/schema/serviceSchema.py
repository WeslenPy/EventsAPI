from app import ma
        
class ServiceSchema(ma.Schema):
    class Meta:
        fields = ('id','name','buy_price','sell_price','amount','symbol','api_id','country_id','color','api_name',
                    'color_hex','country_name','status','number_country','api_url','api_key','url_image')

