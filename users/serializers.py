from rest_framework import serializers
from .models import User
from users.phone_email import is_valid_phone , is_valid_email
from .models import EMAIL,PHONE


class SingUpSeializer(serializers.Serializer):
    phone_or_email = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        phone_or_email = attrs.get('phone_or_email')
        if is_valid_phone(phone_or_email):
            auth_type = PHONE

        elif is_valid_email(phone_or_email):
            auth_type = EMAIL

        else:
           data ={
               "status":False,
               "message":"Enter a valid email or phone number"
           }

           return ValueError(data)
        attrs['auth_type'] = auth_type
        return  attrs
    
    def create(self, validated_data):
        phone_or_email = validated_data['phone_or_email']
        auth_type = validated_data['auth_type']

        if is_valid_phone(phone_or_email):
            User.objects.create(phone_number = phone_or_email, auth_type= auth_type)
        else:
            user = User.objects.create(email=phone_or_email, auth_type=auth_type)

        user.create_code (auth_type)
        validated_data['user'] = user

        return validated_data
    
    def to_representation(self, instance):
        user = instance['user']

        return user.token()



