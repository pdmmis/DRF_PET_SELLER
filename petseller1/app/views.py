from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .permission import IsPetOwnerPermission

# Create your views here.
class AnimalDetails(APIView):
    def get(self,request,pk):
        try:
            queryset=Animal.objects.get(pk=pk)
            queryset.incrementViews()
            serializer=Animalserializer(queryset)
            return Response(
            {
            'status':True,
            'message':'animals fetched by get',
            'data':serializer.data

            })
        except Exception as e:
            print(e)
            return Response(
            {
            'status':False,
            'message':'somthing went wrong',
            'data':serializer.data

            })


class AnimalView(APIView):
    def get(self,request):
        queryset=Animal.objects.all()
        if request.GET.get('search'):
            search=request.GET.get('search')
            queryset=queryset.filter(
                Q(animal_name__icontains=search)|
                Q(animal_description__icontains=search)|
                Q(animal_gender__iexact=search)|
                Q(animal_breed__animal_breed__icontains=search)|
                Q(animal_color__animal_color__icontains=search)
                )
        serializer=Animalserializer(queryset,many=True)
        return Response(
            {
            'status':True,
            'message':'animals fetched by get',
            'data':serializer.data

            }
        )
        


class RegisterAPI(APIView):
    def post(self,request):
        try:
            data=request.data
            serializer=RegisterSerializer(data=data)
            if serializer.is_valid():
                user= User.objects.create(
                    username=serializer.data['username'],
                    email=serializer.data['email']
                      
                )
                user.set_password(serializer.data['password'])
                user.save()
                return Response(
                    {
                    'status':True,
                    'message':'account is created',
                    'data':{},
                    })
            return Response({
                'status':False,
                'message':'keys error',
                'data':serializer.errors
            })
        except Exception as e:
            print(e)

class LoginAPI(APIView):
    def post(self,request):
        try:
            data=request.data
            serializer=LoginSerialzer(data=data)
            if serializer.is_valid():
                user=authenticate(username=serializer.data['username'],password=serializer.data['password'])
                if user:
                    token=Token.objects.get_or_create(user=user) 
                    return Response({
                        'message':'login successfully',
                        'status':'true',
                         'data':{
                        'token':str(token)
                        }

                    })
                return Response({
                    'status':False,
                    'message':'invalid password',
                    'data': serializer.errors

                })
            return Response({
                'status':False,
                'message':'key errors',
                'data':serializer.errors
            })
        except Exception as e:
            print(e)
            return Response({
                'status':False,
                'message':'something went wrong',
                'data':{}

            })
class AnimalCreateAPI(APIView):
    authentication_classes=[TokenAuthentication,]
    permission_classes=[IsAuthenticated,IsPetOwnerPermission]

    def get(self,request):
        queryset=Animal.objects.filter(animal_owner=request.user)
        if request.GET.get('search'):
            search=request.GET.get('search')
            queryset=queryset.filter(
                Q(animal_name__icontains=search)|
                Q(animal_description__icontains=search)|
                Q(animal_gender__iexact=search)|
                Q(animal_breed__animal_breed__icontains=search)|
                Q(animal_color__animal_color__icontains=search)
                )
        serializer=Animalserializer(queryset,many=True)
        return Response(
            {
            'status':True,
            'message':'animals fetched by get',
            'data':serializer.data

            }
        )


    def post(self,request):
         try:
             data=request.data
             data['animal_owner']=request.user.id
             serializer=Animalserializer(data=data)
             if serializer.is_valid():
                 serializer.save()
                 return Response({
                     'status':True,
                     'message':'animal created',
                     'data':serializer.data
                 })
             return Response({
                 'status':False,
                 'message':'Invalid data',
                 'data':serializer.errors
             })
         except Exception as e:
            print(e)
            return Response({
                'status':False,
                'message':'something went wrong',
                'data':{}

            })
    def patch(self,request):
        try:
             data=request.data
             if data.get('id') is None:
                 return Response({
                     'status':False,
                     'message':'id is required',
                     'data':{}
                 })
             animal_obj=Animal.objects.filter(id=data.get('id'))
             if not animal_obj.exists():
                   return Response({
                     'status':False,
                     'message':'invalid animal id',
                     'data':{}
                 })
             animal_obj=animal_obj[0]
             self.check_object_permissions(request,animal_obj)

             data['animal_owner']=request.user.id
             serializer=Animalserializer(data=data)
             if serializer.is_valid():
                 serializer.save()
                 return Response({
                     'status':True,
                     'message':'animal updated',
                     'data':serializer.data
                 })
             return Response({
                 'status':False,
                 'message':'Invalid data',
                 'data':serializer.errors
             })
        except Exception as e:
            print(e)
            return Response({
                'status':False,
                'message':'something went wrong',
                'data':{}

            })