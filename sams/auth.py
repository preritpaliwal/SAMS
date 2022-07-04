from django.contrib.auth import authenticate
import jwt
import datetime
from django.core.mail import EmailMessage
import random
from django.utils import timezone

# from cryptography.fernet import Fernet
from django.utils.encoding import force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .serializers import *
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status



class CheckToken(APIView):
    def get(self,request):
        # print()
        
        token=request.META['HTTP_AUTHORIZATION']
        if(token==None):
            return Response({"message": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        payload = jwt.decode(token, "PP_FROM_KGP", algorithms='HS256')
        user = User.objects.filter(id=int(payload["id"])).first()
        if user is None:
            return Response({"message": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"message": "Valid token"}, status=status.HTTP_200_OK)

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            type = request.data.get('type')
            username = request.data.get('username')
            usertype = False
            user = User.objects.filter(username=username).first()
            userdata=user
            if user is None:
                return Response({"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

            if type == 'manager':
                usertypelocal = ShowManager.objects.filter(user=user).first()
                if usertypelocal:
                    usertype = usertypelocal.is_manager
            elif type == 'clerk':
                usertypelocal = Clerk.objects.filter(user=user).first()
                if usertypelocal:
                    usertype = usertypelocal.is_clerk
            else:
                usertypelocal = Salesperson.objects.filter(user=user).first()
                if usertypelocal:
                    usertype = usertypelocal.is_salesperson
            if (not usertype) or (not (type == 'sales' and usertype)) and (not(type == 'clerk' and usertype)) and (not(type == 'manager' and usertype)):
                return Response({"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

            if user is not None:

                user = authenticate(
                    request,
                    username=request.data["username"],
                    password=request.data["password"],
                )
                if user is not None:
                    payload = {
                        "id": user.id,
                        "type": type,
                        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=12000),
                        "iat": datetime.datetime.utcnow(),
                    }
                    token = jwt.encode(
                        payload, "PP_FROM_KGP", algorithm='HS256')
                    response = Response()

                    serializerdata = UserSerializer(userdata)
                    print(serializerdata.data)
                    alluserdata=serializerdata.data
                    alluserdata['type']=type
                    response.data = {
                        "token": token,
                        "user": alluserdata,
                        "message": "Logged in succesfully",
                    }
                    return response
                else:
                    content = {"message": "Invalid credentials"}
            else:
                content = {"message": "Invalid credentials"}

            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": "some error occurred"+str(e)}, status=status.HTTP_400_BAD_REQUEST)
