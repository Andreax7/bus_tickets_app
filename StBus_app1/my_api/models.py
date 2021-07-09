from django.db import models
from django.contrib.auth.models import AbstractUser

class non_users(models.Model):
    firstname = models.CharField(max_length=64, null=False)
    lastname = models.CharField(max_length=64, null=False)
    email = models.CharField(max_length=64, null=False)
    REQUIRED_FIELDS = [ 'firstname', 'lastname', 'email']
    def __str__(self):
        return self.email

class Profiles(AbstractUser):
    rola = [
        ('none', 'none'),
        ('student', 'student'),
        ('unemployed','unemployed'),
    ]
    email = models.CharField(max_length=64, null=False, unique=True)
    address = models.CharField(max_length=128, blank=True)
    picture = models.ImageField(upload_to='StBus_app1/media', blank=True)
    role = models.CharField(max_length=10, null=False, choices=rola)
    username = models.CharField(max_length=64, null=False, unique=True)
    REQUIRED_FIELDS = ['first_name', 'email', 'password']
    def __str__(self):
        return self.email

class Zones(models.Model):
    zone = models.CharField(max_length=32, null=False, unique=True)
    def __str__(self):
        return self.zone

class Ticket_types(models.Model):
    ttype = [
        ('2h','2h'),
        ('day','day'),
        ]
    tickettype = models.CharField(max_length=3, null=False, choices=ttype)
    ticket_price = models.DecimalField(max_digits=6, decimal_places=2, null=False)
    zone = models.ForeignKey(Zones, on_delete=models.CASCADE, null=False)
    REQUIRED_FIELDS = [ 'tickettype', 'ticket_price', 'zone']
    def __str__(self):
        return str(self.id)

class Single_ticket(models.Model):
    non_users_id = models.ForeignKey(non_users, on_delete=models.CASCADE, null=False)
    Profiles_id = models.ForeignKey(Profiles, on_delete=models.CASCADE, null=True)
    ticket_types_id = models.ForeignKey(Ticket_types, on_delete=models.CASCADE, null=False)
    ticket_date = models.DateTimeField(auto_now_add=True, null=False, editable=False)
    validfrom = models.DateTimeField(auto_now_add=False, null=False, editable=True) #starts expiring
    amount = models.PositiveIntegerField(null=False, default='1')
    def __str__(self):
        return str(self.id)

class Departures(models.Model):
    dtype = [
        ('working_day', 'working_day'),
        ('holidays ', 'holidays'),
    ] 
    deptype = models.CharField(max_length=11, null=False, choices=dtype)
    departure = models.TimeField(auto_now=False,auto_now_add=False, null=True, editable=True) #departure time for holidays
    def __str__(self):
        return str(self.departure)

class Destinations(models.Model):
    zone = models.ForeignKey(Zones, on_delete=models.CASCADE, null=False)
    dest_name = models.CharField(max_length=64, null=False, unique=True)
    dfrom = models.CharField(max_length=64, null=True)
    dto = models.CharField(max_length=64, null=True)
    def get_by_natural_key(self, dest_name):
        return self.get(dest_name=dest_name)
    def __str__(self):
        return self.dest_name

class Timetable(models.Model):
    departure = models.ForeignKey(Departures, on_delete=models.CASCADE, null=False)
    dest_name = models.ForeignKey(Destinations, on_delete=models.CASCADE, null=False)
    def __str__(self):
        return str(self.id)
    objects = Destinations()
    def natural_key(self):
        return (self.dest_name)
    
class Subscription_types(models.Model):
    stype = [
        ('month','month'),
        ('6 months','6 months'),
        ('year','year'),
        ]
    zone = models.ForeignKey(Zones, on_delete=models.CASCADE, null=False)
    subtype = models.CharField(max_length=8, null=False, choices=stype)
    subprice = models.DecimalField(max_digits=6, decimal_places=2, null=False)
    year = models.PositiveIntegerField()
    active = models.BooleanField()
    def __str__(self):
        return str(self.id)
    
class Subscriptions(models.Model):
    Profiles_id = models.ForeignKey(Profiles, on_delete=models.CASCADE, null=False)
    subscription_types_id = models.ForeignKey(Subscription_types, on_delete=models.CASCADE, null=False)
    date_ordered = models.DateTimeField(auto_now_add=True, null=False)
    discount = models.DecimalField(max_digits=6, decimal_places=2, null=False)
    def __str__(self):
        return str(self.id)