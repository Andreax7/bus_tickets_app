from django.contrib import admin
from .models import *

admin.site.register(Profiles)
admin.site.register(non_users)
admin.site.register(Departures)
admin.site.register(Destinations)
admin.site.register(Ticket_types)
admin.site.register(Zones)
admin.site.register(Timetable)
admin.site.register(Single_ticket)
admin.site.register(Subscriptions)
admin.site.register(Subscription_types)