from . import views
from django.urls import path, include
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token


router = routers.DefaultRouter(trailing_slash=False)

urlpatterns = [
    #Registered Users
    path('myprofile/', views.ProfileView, name='profile'),
    path('auth/', obtain_jwt_token),
    path('refresh/', refresh_jwt_token),
    path('verify/', verify_jwt_token),
 #   path('rest-auth/', include('rest_framework.urls')),
  
     # everyone 
    path('destinations/', views.AllDestinations, name='destinations'),
    path('destinations/<int:pk>', views.DestZone, name='destinations_by_zone'), # filter destinations by zone
    path('timetable/<int:did>', views.Show_Timetable), # gets the timetable of chosen destination
   
    path('register/', views.RegisterAPI.as_view(), name='register'), 
    path('checkuser/<str:username>',views.CheckusernameAPI), # does username exists -for login/register
    path('checkmail/<str:email>',views.CheckemailAPI), #does email exists - register check
    path('nonusers/', views.nonUser), #for ticket creating
    path('buy_ticket/', views.Buy_Ticket),
    path('ttype/', views.tickettyp), # gets all ticket types or admin creats new ticket type

    #Admin
    path('dests/',views.CreateDestination),
    path('dests/<int:pk>', views.Destination_Update),
    path('isstaff/', views.Isadmin),
    path('addept/', views.AddDeparture),
    path('deldep/<int:pk>', views.DeleteDeparture),
    path('newtimetable/', views.CreateTimetable), #Post
    path('deltimetable/<int:dnid>/<int:did>', views.DeleteTimetable),
    path('showtimetable/<int:did>', views.ShowTimetable),
    path('ticketactive/<int:pk>',views.TicketDeactivate),
    path('nuticket/<int:nuid>', views.nUserTicket),
    path('soldtickets/<int:tid>', views.soldTickets),
    path('allprofiles/', views.AllProfiles),
    path('setemploy/<int:eid>', views.SetEmployee),
    path('getusersub/<int:uid>', views.GetUserSubsciption),
    path('editsub/<int:sid>', views.EditSubscription),
    path('allsubs/', views.SubTypes),
    path('editsubtype/<int:pk>', views.EditSubType),
    path('soldsubs/<int:id>',views.soldSubscriptions), #GET
]