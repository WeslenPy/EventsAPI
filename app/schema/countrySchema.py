from app import ma

class CountrySchema(ma.Schema):
    class Meta:
        fields = ('id','country_name','number_country')
        
