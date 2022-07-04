from rest_framework.response import Response
import jwt
from .views import *
from .models import *
from rest_framework import status

def unauthenticated_user(view_func):
    def wrapper_func(request,*args, **kwargs):
        token = request.data.get('token')
        
        print(token)
        if not token:
            return Response('Unauthenticated', status=status.HTTP_401_UNAUTHORIZED)
        else:
            try:
                payload = jwt.decode(token, "PP_FROM_KGP", algorithms='HS256')
            except jwt.ExpiredSignatureError:
                return Response('Token expired',status=status.HTTP_401_UNAUTHORIZED)
        user = User.objects.filter(id=int(payload['id'])).first()
        if user is None:
            return Response('Invalid token')
        return view_func(request,user)

    return wrapper_func


def get_protection(view_func):
    def wrapper_func(request, *args, **kwargs):
        token=request.META['HTTP_AUTHORIZATION']
        if(token==None):
            return Response({"message": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        payload = jwt.decode(token, "PP_FROM_KGP", algorithms='HS256')
        user = User.objects.filter(id=int(payload["id"])).first()
        if user is None:
            return Response({"message": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        return view_func(request,user)

    return wrapper_func

