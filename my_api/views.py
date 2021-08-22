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
from django.db.models import Count

 
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
    if request.method == 'GET' and (request.user).is_staff == True: #admin can see all nonusers that used tickets
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
        serializer = TicketTypeSerializer(data=request.data, many=True)
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

@api_view(['POST', 'GET'])
@permission_classes([AllowAny])
def Buy_Ticket(request):
    if request.method == 'GET' and (request.user).is_staff == True:
        queryset = Single_ticket.objects.exclude(non_users_id__isnull = True)
        serializer = TicketSerializer(queryset, many= True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'POST':
        serializer = TicketSerializer(data = request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors)

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
        dests = Destinations.objects.filter(active=True).order_by("line_no")
        serializer = DestDetailSerializer(dests, many=True)
        return Response(serializer.data)


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
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET'])
@permission_classes([AllowAny])       
def DestZone(request,pk): # Gets all destinations in chosen zone from db 
    dest_by_zone = Destinations.objects.filter(zone_id=pk, active=True)
    if request.method == 'GET':
        serializer = DestDetailSerializer(dest_by_zone, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 


#**************************************************************************************
#*******************************ADMIN PANEL********************************************
#**************************************************************************************


@permission_classes([IsAdminUser, IsAuthenticated])
@api_view(['PUT'])
def SetEmployee(request, eid): #admin api endpoint for declaring user with profile as admin/employee or not
    try: 
        Profile = Profiles.objects.get(id=eid)
    except Profile.DoesNotExist: 
        return Response({'message': 'User with this profile does not exist'}, status=status.HTTP_404_NOT_FOUND) 
    if request.method == 'PUT':
        serializer = SetEmployeeSerializer(Profile, data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_401_UNAUTHORIZED)

@permission_classes([IsAdminUser, IsAuthenticated])
@api_view(['GET'])
def GetUserSubsciption(request, uid): #admin api endpoint for declaring user with profile as admin/employee or not
    if request.method == 'GET':
        subs = Subscriptions.objects.filter(Profiles_id_id=uid)
        serializer = SubscriptionSerializer(subs,  many=True)
        return Response(serializer.data)
    return Response(status=status.HTTP_401_UNAUTHORIZED)

@permission_classes([IsAdminUser, IsAuthenticated])
@api_view(['PUT','GET'])
def EditSubscription(request,sid):
    if request.method == 'GET':
        subs = Subscriptions.objects.filter(id=sid)
        serializer = SubscriptionSerializer(subs,  many=True)
        return Response(serializer.data)
    if request.method == 'PUT':
        subs = Subscriptions.objects.get(id=sid)
        serializer = SubscriptionSerializer(subs, data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_401_UNAUTHORIZED)


@permission_classes([IsAdminUser, IsAuthenticated])
@api_view(['GET','POST'])
def SubTypes(request):
        if request.method == 'GET':
            subs = Subscription_types.objects.all()
            serializer = SubTypeSerializer(subs,  many=True)
            return Response(serializer.data)
        if request.method == 'POST':
            serializer = SubTypeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes([IsAdminUser, IsAuthenticated])
@api_view(['PUT'])
def EditSubType(request, pk):
    if request.method == 'PUT':
        subs = Subscription_types.objects.get(id=pk)
        serializer = SubTypeSerializer(subs, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data)
        return Response(serializer.errors)
    
    
@api_view(['GET'])
@permission_classes([IsAdminUser])
def AllProfiles(request):
    if request.method == 'GET':
        profiles = Profiles.objects.all()
        serializer = AdminSerializer(profiles, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def CreateDestination(request):
    user = request.user
    if request.method == 'GET':
        dests = Destinations.objects.all().order_by('line_no')
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
@api_view(['GET', 'PUT'])
def Destination_Update(request,pk):  #admin api endpoint for update choosen destination
    try: 
        dest = Destinations.objects.get(id=pk)
    except dest.DoesNotExist: 
        return Response({'message': 'Destination does not exist'}, status=status.HTTP_404_NOT_FOUND) 
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
   # if request.method == 'DELETE':
   #     dest.delete()
   #    return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_401_UNAUTHORIZED)


@permission_classes([IsAdminUser, IsAuthenticated])
@api_view(['GET','POST'])
def AddDeparture(request): #Adds and gets all departures
    departures = Departures.objects.all().order_by('departure')
    if request.method == 'GET':
        serializer = DeparturesSerializer(departures, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = DeparturesSerializer(data=request.data, context={"request": request}) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.data)

@permission_classes([IsAdminUser, IsAuthenticated])
@api_view(['DELETE'])
def DeleteDeparture(request,pk): # delete chosen departure
    departures = Departures.objects.get(id=pk)
    serializer = DeparturesSerializer(departures)
    if departures:
        departures.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(serializer.data)

@permission_classes([AllowAny])
@api_view(['GET'])
def Isadmin(request): #this function is querying db if user is staff or not
    user = request.user
    if user.is_staff:
        return Response({'true'})
    return Response({'false'})

@permission_classes([IsAdminUser, IsAuthenticated])
@api_view(['POST'])
def CreateTimetable(request):
     if request.method == 'POST':
        serializer = TimetableSerializer(data=request.data, context={"request": request}) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

@permission_classes([IsAdminUser, IsAuthenticated])
@api_view(['POST', 'DELETE'])        
def DeleteTimetable(request,dnid,did):
    dest = Timetable.objects.filter(dest_name_id = dnid, departure_id=did)
    if dest:
        dest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@permission_classes([IsAdminUser, IsAuthenticated])
@api_view(['GET'])
def ShowTimetable(request,did):
    timetable = Timetable.objects.filter(dest_name_id=did)
    serialize = TimetableSerializer(timetable, many=True)
    return Response(serialize.data, status=status.HTTP_200_OK)

@permission_classes([IsAdminUser, IsAuthenticated])
@api_view(['PUT'])
def TicketDeactivate(request,pk):  #admin api endpoint for ticket type activation/deactivation
    try: 
        ticket = Ticket_types.objects.get(id=pk)
    except ticket.DoesNotExist: 
        return Response({'message': 'Ticket type does not exist'}, status=status.HTTP_404_NOT_FOUND) 
    if request.method == 'PUT':
        serializer = TicketTypeSerializer(ticket, data=request.data, partial=True)
        if serializer.is_valid():                       
            serializer.save() 
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_401_UNAUTHORIZED)

@permission_classes([IsAdminUser, IsAuthenticated])
@api_view(['GET'])
def nUserTicket(request, nuid):
    try: 
        tickets = Single_ticket.objects.filter(non_users_id=nuid)
    except ticket.DoesNotExist: 
        return Response({'message': 'Ticket type does not exist'}, status=status.HTTP_404_NOT_FOUND) 
    if request.method == 'GET':
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Number of sold tickets per ticket type
@permission_classes([IsAdminUser, IsAuthenticated])
@api_view(['GET'])
def soldTickets(request, tid):     
    if request.method == 'GET':
        cnt = []
        total = 0
        tickets = Single_ticket.objects.filter(ticket_types_id=tid).values('amount').annotate(count=Count('amount'))
        for t in tickets:
            var = t["amount"] * t["count"]
            total =+ var
            cnt.append(total)       
        return Response( sum(cnt), status=status.HTTP_200_OK)
    return Response({'message': 'Ticket type does not exist'}, status=status.HTTP_404_NOT_FOUND)

# Number of sold subscriptions per sub. type
@permission_classes([IsAdminUser, IsAuthenticated])
@api_view(['GET'])
def soldSubscriptions(request, id):
    if request.method == 'GET':
        subs = Subscriptions.objects.filter(subscription_types_id=id).count()
        return Response( subs, status=status.HTTP_200_OK)
    return Response({'message': 'Subscription type does not exist'}, status=status.HTTP_404_NOT_FOUND)

    
#*****************************************************************
#****************************USER PANEL***************************
#*****************************************************************

@api_view(['GET','PUT'])
@permission_classes([IsAuthenticated])
def ProfileView(request, format=None):
    user=str(request.user)
    data=Profiles.objects.filter(email=request.user)
    serializer=UserProfileSerializer(data, many=True)
    return Response(serializer.data)
