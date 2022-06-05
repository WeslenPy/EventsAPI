from app import ma

class UserSchema(ma.Schema):
    created_at = ma.DateTime(format='%d/%m/%Y H %H:%M:%S')
    class Meta:
        fields = ('id','cpf','first_name','last_name','email','balance',
                            'created_at','blocked_time','cancellation_count')
