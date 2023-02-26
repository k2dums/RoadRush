from rest_framework import serializers
from .models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed

class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(max_length=68,min_length=6,write_only=True) #write_only allows only to write, not for user to read

    class Meta:
        model=User
        fields=['email','username','password'] #since we said the password is write only, send back response using this email and you won't get password

    def validate(self,attrs):
        email=attrs.get('email','')
        username=attrs.get('username','')
        if not username.isalnum():
            raise serializers.ValidationError('The username should only contain alphanumric characters')
        return attrs
        
    #create gets called when calling serializer.save()
    def create(self, validated_data):
       return User.objects.create_user(**validated_data) #make sure to pass kargs or will send only the username

class EmailVerificationSerializer(serializers.ModelSerializer):
    token=serializers.CharField(max_length=555)#token field to show token needed

    class Meta:
        model=User
        fields=['token']

class LoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255,min_length=3)
    password=serializers.CharField(max_length=68,min_length=6,write_only=True)#so that it doesnt send it back to the user
    username=serializers.CharField(max_length=255,min_length=3,read_only=True)#dont want the user to provide usernmae
    tokens=serializers.CharField(max_length=68,min_length=6,read_only=True)

    #we need to setup meta which model we want
    class Meta:
        model=User
        fields=['email','password','username','tokens']

    def validate(self, attrs):
        email=attrs.get('email','')
        password=attrs.get('password','')
        user=auth.authenticate(email=email,password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account Disabled, contact CustomerCare')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')
        return {
            'email':user.email,
            'username':user.username,
            'tokens':user.tokens()
        }
        
