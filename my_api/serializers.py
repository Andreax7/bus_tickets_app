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
        user.set_password(validated_data['password'])
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

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    class Meta:
        model = Profiles
        fields = ['id','username','first_name','last_name','address','picture','role','is_active']
    def validate(self, validated_data):
            return Profiles(**validated_data)
    

class DestDetailSerializer(serializers.ModelSerializer):
    zone = serializers.CharField(source='zone.zone')
    class Meta:
        model = Destinations
        fields = ['id','zone','dfrom','dto']

# Timetable data
class TimetableSerializer(serializers.ModelSerializer):
    departure = serializers.CharField(source='departure.departure')
    deptype = serializers.CharField(source='departure.deptype')
    class Meta:
        model = Timetable
        fields = ['dest_name','departure', 'deptype']
    def natural_key(self):
        return (self.dest_name)

#Non user ticket buying
class nonusrSerializer(serializers.ModelSerializer):
    class Meta:
        model = non_users
        fields = '__all__'

class TicketSerializer(serializers.ModelSerializer):
    ticketype = serializers.CharField(source='ticket_types.ticketype')
    ticketprice = serializers.CharField(source='ticket_types.ticket_price')
    zone = serializers.CharField(source='ticket_types.zone_id')
    email = serializers.CharField(source='non_users.email')
    email = serializers.CharField(source='profiles.email')
    class Meta:
        model = Single_ticket
        fields = ['ticketype', 'validfrom','amount','ticketprice','zone','email' ]
    def create(self, validated_data):
        email = validated_data['ticket_type']
        ticket = Single_ticket.objects.create(
                Ticket_types = validated_data['ticket_type'],
                validfrom = validated_data['validfrom'], 
                amount = validated_data['amount'])
        ticket.save()

#**************************************************************************************
#*******************************ADMIN PANEL********************************************
#**************************************************************************************