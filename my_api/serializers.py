from rest_framework import serializers
from .models import *
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework.response import Response
from rest_framework.fields import CurrentUserDefault

#RegisterSerializer whole Form validation
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=Profiles.objects.all())])
    username = serializers.CharField(required=True, validators=[UniqueValidator(queryset=Profiles.objects.all())])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = Profiles
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'password2', 'role')
        extra_kwargs = {
            'username': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'role': {'default': None}}
    def validate(self, value): #Validator for matching password
        if value['password'] != value['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return value
    def create(self, validated_data):
        user = Profiles.objects.create(username = validated_data['username'], 
                        first_name = validated_data['first_name'],
                        last_name = validated_data['last_name'],
                        email = validated_data['email'],
                        password = validated_data['password'],
                        role = validated_data['role'])
        user.set_password(validated_data['password']) # creates hashed password
        user.save() 
        return user

 


#------------------User profile data email and username validation --------------------------
class usernameSerializer(serializers.ModelSerializer):
    username = serializers.CharField(validators=[UniqueValidator(queryset=Profiles.objects.all())])
    class Meta:
        model = Profiles
        fields = ['username']
        def validate(self, value):
            user = value['username']
            if username == value['username']:
                raise serializers.ValidationError({'Allready Exists'})
                
class emailSerializer(serializers.ModelSerializer):
    email = serializers.CharField(validators=[UniqueValidator(queryset=Profiles.objects.all())])
    class Meta:
        model = Profiles
        fields = ['email']
        def validate(self, value):
            user = value['email']
            if str(email) == str(user):
                raise serializers.ValidationError({'Allready Exists'})          
 #------------------User profile data email and username validation --------------------------       

#*****************************************************
#***************USER PANEL****************************
#*****************************************************
class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    class Meta:
        model = Profiles
        fields = ['id','username','first_name','last_name', 'email', 'address','picture','role']
    def validate(self, validated_data):
            return Profiles(**validated_data)
    
class DestDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destinations
        fields = '__all__'
    def create(self, validated_data):
        dest = Destinations.objects.create(**validated_data) # creates hashed password
        dest.save() 
        return dest

# Timetable data
class TimetableSerializer(serializers.ModelSerializer):
    departure = serializers.CharField(source='departure.departure')
    deptype = serializers.CharField(source='departure.deptype')
    class Meta:
        model = Timetable
        fields = ['dest_name','departure', 'deptype']
    def natural_key(self):
        return (self.dest_name)

#************************************************
# #**************Non user ticket CREATE**********
class nonusrSerializer(serializers.ModelSerializer):
    class Meta:
        model = non_users
        fields = '__all__'
        def create(self, validated_data):
            user = non_users.objects.create(
                        firstname = validated_data['firstname'],
                        lastname = validated_data['lastname'],
                        email = validated_data['email'])
            user.save() 
            return user
        def validate(self, validated_data):
            user = non_users.objects.get(email = validated_data['email'])
            return user

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        ticket_date = models.DateTimeField(auto_now_add=True)
        model = Single_ticket
        fields = "__all__"
   



#**************************************************************************************
#*******************************ADMIN PANEL********************************************
#**************************************************************************************

class AdminSeralizer(serializers.ModelSerializer):
    is_staff = serializers.CharField
    class Meta:
        model = Profiles
        fields = ['id','username', 'is_active', 'is_staff', 'last_login' ]
    def validate(self,validated_data):
        return Profiles(**validated_data)

class DeparturesSerializer(serializers.ModelSerializer):
    class Meta:
        models = Departures
   

class TicketTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket_types
        fields = '__all__'
    def create(self, validated_data):
        ticket = Ticket_types.objects.create(
                tickettype = validated_data['tickettype'],
                ticket_price = validated_data['ticket_price'], 
                zone = validated_data['zone'])
        ticket.save()
        return ticket
    def update(self, instance, validated_data):
        instance.tickettype = validated_data.get('tickettype', instance.tickettype)
        instance.ticketprice = validated_data.get('ticketprice', instance.ticketprice)
        instance.zone_id = validated_data.get('zone', instance.zone)
        return instance

        def validate(self, validated_data):
            return Ticket_types(**validated_data)