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
    class Meta:
        model = Profiles
        fields = ['id','username','first_name','last_name', 'email', 'address','picture','role']
    def validate(self, validated_data):
            return Profiles(**validated_data)

class EditProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profiles
        fields = ['username','first_name','last_name', 'email', 'address','picture','role']


class ProfileCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profiles
        fields = ['id', 'email']
    def validate(self, validated_data):
            return Profiles(**validated_data)

    

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
    ticket_date = serializers.DateTimeField(read_only=True)
    class Meta:
        model = Single_ticket
        fields = ["id","non_users_id","Profiles_id","ticket_types_id","amount","validfrom","ticket_date"]



#**************************************************************************************
#*******************************ADMIN PANEL********************************************
#**************************************************************************************

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profiles
        fields = '__all__'
    def validate(self,validated_data):
        return Profiles(**validated_data)
    def create(self, validated_data):
        profile = Profiles.objects.create(**validated_data)
        profile.save()
        return profile

class SetEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profiles
        fields = ['id','is_staff','is_active']
    def create(self, validated_data):
        profile = Profiles.objects.create(**validated_data)
        profile.save()
        return profile

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriptions
        fields = '__all__'
    def create(self, validated_data):
        subs = Subscriptions.objects.create(**validated_data)
        subs.save() 
        return subs

class SubTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription_types
        fields = '__all__'

class DeparturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departures
        fields = '__all__'

# Timetable data
class TimetableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timetable
        fields = '__all__'
    def create(self, validated_data):
        dest = Timetable.objects.create(**validated_data)
        dest.save() 
        return dest


class DestDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destinations
        fields = '__all__'
    def create(self, validated_data):
        dest = Destinations.objects.create(**validated_data)
        dest.save() 
        return dest
        
class TicketTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket_types
        fields = '__all__'
    def create(self, validated_data):
        ticket = Ticket_types.objects.create(**validated_data)
        ticket.save()
        return ticket
    