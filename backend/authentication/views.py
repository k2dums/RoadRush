from django.shortcuts import render
from .serializers import RegisterSerializer,EmailVerificationSerializer,LoginSerializer
from rest_framework.response import Response
from rest_framework import generics,status,views
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
# from drf_yasg.utils import swagger_auto_schema
# from drf_yasg import openapi
class RegisterView(generics.GenericAPIView):
    serializer_class=RegisterSerializer
    def post(self,request):
        user=request.data
        serializer=self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)#to make sure it validates it, runs validate
        serializer.save()#will run create

        user_data=serializer.data #once the user is saved will be returning the user

        #we need to create a token for the user and send it to the email
        #defining token
        user=User.objects.get(email=user_data['email'])
        #actually gives two token refresh and access
        token=RefreshToken.for_user(user)
        access_token=token.access_token
        current_site=get_current_site(request).domain  #returns the domain like goggle.com without the protocol http
        relative_link=reverse('email-verify')#for redirection
        # click link on the email and the link should bring them back to the application, to get link/domain we need to use site framework
        absurl='http://'+current_site+relative_link+'?token='+ str(access_token)
        email_body='Hi, ' + user.username + '\nUser link below to verify your email\n'+absurl
        #data being send via email
        data={'email_body':email_body,'email_subject':'Verify the email','email_to':user.email.rstrip()}
        Util.send_email(data)
  
        #Now we can tell the account was created
        return Response(user_data,status=status.HTTP_201_CREATED)


#redirect the user
#we need serializer class that exposes some fields to the view
#a special case for API  view that is why not genricApiView
#we need swagger which field to create
class VerifyEmail(views.APIView):
    serializer_class=EmailVerificationSerializer
    # token_param_config=openapi.Parameter('token',in_=openapi.IN_QUERY,description='Description',type=openapi.TYPE_STRING)#open api, this has to be here before open api
    # @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self,request):
        token=request.GET.get('token') # as the token is in the query parameter of token
        try:#trying to decode the token
            #encoding is done using the applciation secret key
            #if valid should give the date that was encoded
            payload=jwt.decode(token,settings.SECRET_KEY,algorithms=["HS256"])
            user=User.objects.get(id=payload['user_id'])#payload uses key user_id
            #now the user is verified
            if not user.is_verified:
                user.is_verified=True
                user.save()
            return Response({'email':'Sucessfully verified'},status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError: # jwt token is expired
            return Response({'error':'activation link expired'},status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError: #when user has tampered with the token
            return Response({'error':'Invalid Token'},status=status.HTTP_400_BAD_REQUEST)

class LoginApiView(generics.GenericAPIView):
    serializer_class=LoginSerializer
    def post(self,request):
        user=request.data
        serializer=self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)#does the authentication
        #need the response

        return Response(serializer.data,status=status.HTTP_200_OK)