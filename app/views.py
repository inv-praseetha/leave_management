from django.urls import resolvers
from django.contrib.auth import authenticate
from app.permission import IsAdmin
from rest_framework.views import APIView
from .serialaizers import UserSerialaizer
from rest_framework.response import Response
from rest_framework import status
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.
class CreatingUser(APIView):
    permission_classes=[IsAdmin]
    def post(self,request):
        
        print("the view has been hit")
        if request.data['role'] not in User.Role:
            return Response("invalid role please add a valid role",status=status.HTTP_400_BAD_REQUEST)
        if request.data['department'] not in User.Department:
            return Response("invalid department please add a valid department",status=status.HTTP_400_BAD_REQUEST)
        if request.data['role'] == User.Role.EMPLOYEE:
            manager_id=request.data.get('manager_id')
            if manager_id is None:
                return Response("manager id is required",status=status.HTTP_400_BAD_REQUEST)
            try:
                manager=User.objects.get(id=manager_id)
            except User.DoesNotExist:
                return Response("manager not found",status=status.HTTP_404_NOT_FOUND)   
        data=UserSerialaizer(data=request.data,context={"request":request})
        print(data)
        if data.is_valid():
            data.save()

            return Response(data.data,status=status.HTTP_201_CREATED)
        return Response(data.errors,status=status.HTTP_400_BAD_REQUEST)
    def get(self,request):
        data=User.objects.all().order_by("-id")
        print("objectssss....",data)
        for i in data:
            print(i.username)
        datas=UserSerialaizer(data,many=True)
        print("......s",datas)
        return Response(datas.data,status=status.HTTP_200_OK)
class UserUPdateDetail(APIView):
    permission_classes=[IsAdmin]
    def get(self,request,id):
        try:
            instance=User.objects.get(id=id)
            if instance:
               data=UserSerialaizer(instance)
            return Response(data.data,status=status.HTTP_200_OK)    
        except User.DoesNotExist:
            return Response("user not found",status=status.HTTP_404_NOT_FOUND) 

    def put(self,request,id):
        try:
            instance=User.objects.get(id=id)
            if instance:
                print("this instance is found:",instance)
                data=UserSerialaizer(instance,request.data)
                if data.is_valid():
                    data.save()
                       
                print("this data is",data)
                print("this data errors",data.errors)
            return Response(data.data,status=status.HTTP_200_OK)    
        except User.DoesNotExist:
            return Response("user not found",status=status.HTTP_404_NOT_FOUND)
class LoginAPIview(APIView):
    def post(self,request):
        email=request.data.get('email')
        password=request.data.get('password')
        user=authenticate(request,email=email,password=password)
        print(user)
        if user is None:
            return Response({"message":"invalid credentials"},status=status.HTTP_401_UNAUTHORIZED)
        refresh=RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user_id": user.id,
            "email": user.email,
            "role": user.role,
        }, status=status.HTTP_200_OK)
      

    

