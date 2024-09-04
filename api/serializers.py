from rest_framework import serializers
from django.contrib.auth import authenticate
from accounts.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from products.models import Product



class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('id','username','password','first_name','last_name','email',)
        
class LoginSerializers(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self,data):
        username = data.get('username')
        password = data.get('password')
        
        if username and password:
           # user = authenticate(username=username,password=password)
            if user:=authenticate(username=username,password=password):
                data['user']=user
            else:
                raise serializers.ValidationError('Invalid Credentials')
        else:
            raise serializers.ValidationError("Both Field Required")
        return data
        
        
        
class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        