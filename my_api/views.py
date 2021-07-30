from django.shortcuts import render
from django.contrib.auth import get_user_model
from .serializers import *
from .models import *
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.generics import CreateAPIView
from django.views.decorators.csrf import csrf_exempt, csrf_protect, ensure_csrf_cookie
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import IsAdminUser
from django.shortcuts import render

 
#*****************************************************************
#***************************ALL USERS*****************************
#*****************************************************************

# ------POST METHODS----------
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
             #   token = Token.objects.create(user=user)  Used for TokenBasedAuth not JWT!
                json = serializer.data
               # json['token'] = token.key  Used for TokenBasedAuth not JWT!
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#--------------------------------------------------------------
#-----------------CREATE AND GET BUS TICKETS-------------------
@api_view(['GET', 'POST']) # Check if user allready had ticket to prevent duplicates
@permission_classes([AllowAny])
@csrf_exempt
def nonUser(request):
    if request.method == 'GET' and (request.user).is_staff == True: #admin can see all users that used tickets
        #nuser = non_users.objects.filter()
        data = non_users.objects.all()
        serializer = nonusrSerializer(data, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = nonusrSerializer(data=request.data)
        email=request.data['email']
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif non_users.objects.get(email=email) != None:
            queryset = non_users.objects.get(email=email)
            serializer = nonusrSerializer(queryset)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
@csrf_exempt
def tickettyp(request):
    if request.method == 'POST' and (request.user).is_staff == True:
        serializer = TicketTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        queryset = Ticket_types.objects.all()
        serializer = TicketTypeSerializer(queryset, many=True)
        return Response(serializer.data)
    return Response(status=status.HTTP_400_BAD_REQUEST)

#Non_user ticket buying

@api_view(['POST'])
@permission_classes([AllowAny])
def Buy_Ticket(request):
    if request.method == 'POST':
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#---------------------Check if user allready exists api endpoint (used for verification)
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
#------------------------------------------------

#--------GET METHODS ----------

@api_view(['GET'])
@permission_classes([AllowAny])
def AllDestinations(request):
    if request.method == 'GET':
        dests = Destinations.objects.filter(active=True)
        serializer = DestDetailSerializer(dests, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])       
def DestZone(request,pk): # Gets all destinations in chosen zone from db 
    dest_by_zone = Destinations.objects.filter(zone_id=pk, active=True)
    if request.method == 'GET':
        serializer = DestDetailSerializer(dest_by_zone, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET']) 
@permission_classes([AllowAny])
def Show_Timetable(request,did):
    timetable = Timetable.objects.filter(dest_name_id=did)
    departures = Departures.objects.all().order_by('departure')
    filtered_timetable=[]
    if request.method == 'GET':
        for d in departures:
            time=timetable.filter(departure_id=d.id)
            for dep in time:
                filtered_timetable.append({d.deptype:d.departure})
        return Response(filtered_timetable, status=status.HTTP_200_OK)   


#**************************************************************************************
#*******************************ADMIN PANEL********************************************
#**************************************************************************************

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def AdminProfileView(request, format=None):
    user = str(request.user)
    data = Profiles.objects.filter(is_staff=True)
    serializer = AdminSeralizer(data, many=True)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def CreateDestination(request):
    user = request.user
    if request.method == 'GET':
        dests = Destinations.objects.all()
        serializer = DestDetailSerializer(dests, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = DestDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@permission_classes([IsAdminUser])
@api_view(['GET', 'PUT', 'DELETE'])
def Destination_Update(request,pk):  #admin api endpoint for update and delete choosen destination
    try: 
        dest = Destinations.objects.get(id=pk)
    except dest.DoesNotExist: 
        return JsonResponse({'message': 'Destination does not exist'}, status=status.HTTP_404_NOT_FOUND) 
    if request.method == 'GET':
        dest = Destinations.objects.get(id=pk)
        serializer = DestDetailSerializer(dest)
        return Response(serializer.data)
    if request.method == 'PUT':
        serializer = DestDetailSerializer(dest, data=request.data, partial=True)
        if serializer.is_valid():                       
            serializer.save() 
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        dest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_401_UNAUTHORIZED)

@permission_classes([IsAdminUser, IsAuthenticated])
@api_view(['PUT','DELETE'])
def EditDest(request, id):
    dest = Destinations.objects.get(id=pk)
    serializer = DestDetailSerializer(dest)
    return Response(serializer.data)

@permission_classes([IsAdminUser, IsAuthenticated])
@api_view(['PUT','DELETE'])
def EditDep(request, id):
    dest = Departures.objects.get(id=pk)
    serializer = DestDetailSerializer(dest)
    return Response(serializer.data)

@permission_classes([IsAdminUser, IsAuthenticated])
@api_view(['GET','POST'])
def AddDeparture(request): #Adds and gets all departures
    departures = Departures.objects.all().order_by('departure')
    serializer = DeparturesSerializer(dest)
    return Response(serializer.data)

@permission_classes([IsAdminUser, IsAuthenticated])
@api_view(['GET'])
def Isadmin(request): #this function is querying db if user is staff or not
    user = request.user
    if user.is_staff:
        return Response({'true'})
    return Response({'false'})


#*****************************************************************
#****************************USER PANEL***************************
#*****************************************************************

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def ProfileView(request, format=None):
    user =str(request.user)
    data=Profiles.objects.filter(email=request.user)
    serializer=UserProfileSerializer(data, many=True)
    return Response(serializer.data)
