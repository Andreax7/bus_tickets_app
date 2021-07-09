from django.shortcuts import render
from django.core import serializers as core_serializers
from .serializers import *
from .models import *
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.generics import CreateAPIView
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import IsAdminUser
from django.shortcuts import render
 
#*****************************************************************
#***************************ALL USERS*****************************
#*****************************************************************

# ------POST METHODS----------
#Login 
class ProfileView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, format='json'):
        content = {
            'user': str(request.user),
            'auth': str(request.auth),
        }
        return Response(content)

#Registration

class RegisterAPI(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = Profiles.objects.all()
    serializer_class = RegisterSerializer
    def post(self, request, format='json'):
        serializer = RegisterSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token = Token.objects.create(user=user)
                json = serializer.data
                json['token'] = token.key
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def CheckusernameAPI(request,username):
    data=Profiles.objects.filter(username=username)
    serializer=usernameSerializer(data, many=True)
    uname = ''
    for i in data:
        uname=i.username
    if uname == str(username):
        return Response('true')
    return Response('false')

@api_view(['GET'])
@permission_classes([AllowAny])
@csrf_exempt
def CheckemailAPI(request,email):
    data=Profiles.objects.filter(email=email)
    serializer=emailSerializer(data, many=True)
    usr = ''
    for i in data:
        print(data)
        usr=i.email
    if usr == str(email):
        return Response('true')
    return Response('false')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ProfileView(request, format=None):
    content = {
        'user': str(request.user),  # `django.contrib.auth.User` instance.
        'auth': str(request.auth),  # None
    }
    return Response(content)

class JSONWebTokenAPIView(APIView):
    permission_classes = ()
    authentication_classes = ()
    def get_serializer_context(self):
        return {
            'request': self.request,
            'view': self,
        }
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            response_data = jwt_response_payload_handler(token, user, request)
            response = Response(response_data)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() +
                              api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                    token,
                                    expires=expiration,
                                    httponly=True)
            return Response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#--------GET METHODS ----------

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def AllDestinations(request):
    user = request.user
    if request.method == 'GET':
        dests = Destinations.objects.all()
        serializer = DestDetailSerializer(dests, many=True)
        return Response(serializer.data)
    elif request.method == 'POST' and user.is_staff == True:
        serializer = DestDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])       
def DestZone(request,pk):
    dest_by_zone = Destinations.objects.filter(zone_id=pk)
    if request.method == 'GET':
        serializer = DestDetailSerializer(dest_by_zone, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST']) 
@permission_classes([AllowAny])
def Show_Timetable(request,did):
    timetable = Timetable.objects.filter(dest_name_id=did)
    dest = Destinations.objects.get(id=did)
    departures = Departures.objects.all()
    filtered_timetable=[]
    if request.method == 'GET':
        for t in timetable:
            time=Departures.objects.filter(id=t.departure.id)
            for dep in time:
                filtered_timetable.append({dep.deptype:dep.departure})
        return Response(filtered_timetable, status=status.HTTP_200_OK)   
    if request.method == 'POST':

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Non_user ticket buying
@api_view(['GET','POST'])
def Buy_Ticket(request,tid):
    user = request.user
    if request.method == 'POST':
        serializer = TicketSerializer(ticket, many=True)
        ticket = Ticket_types.objects.filter(ticket_types_id=tid)
        return Response(serializer.data)
    return Response(status=status.HTTP_400_BAD_REQUEST)

#**************************************************************************************
#*******************************ADMIN PANEL********************************************
#**************************************************************************************

@permission_classes([IsAdminUser, IsAuthenticated])
@api_view(['GET'])
def DestDetail(request,pk):
    if request.method == 'GET' and request.user.is_staff == True:
        dest = Destinations.objects.get(id=pk)
        serializer = DestDetailSerializer(dest)
        return Response(serializer.data)
    elif Destinations.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_401_UNAUTHORIZED)


@permission_classes([IsAdminUser])
@api_view(['GET', 'PUT', 'DELETE'])
def Destination_Update(request,pk):
    user = request.user
    if request.method == 'GET' and user.is_staff == True:
        dest = Destinations.objects.get(id=pk)
        serializer = DestDetailSerializer(dest)
        return Response(serializer.data)
    elif request.method == 'PUT' and user.is_staff == True:
        serializer = DestinationSerializer(dests, data=request.data)
        if serializer.is_valid():                       
            serializer.save() 
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE' and user.is_staff == True:
        dests.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_401_UNAUTHORIZED)

#*****************************************************************
#****************************USER PANEL***************************
#*****************************************************************