from . import views
from django.urls import path, include
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

router = routers.DefaultRouter(trailing_slash=False)

urlpatterns = [
    path('accounts/profile/', views.ProfileView, name='profile'),
    path('auth/', obtain_jwt_token),
    path('token-refresh/', refresh_jwt_token),
    
    path('register/', views.RegisterAPI.as_view(), name='register'),
    path('checkuser/<str:username>',views.CheckusernameAPI),
    path('checkmail/<str:email>',views.CheckemailAPI),

    #Admin
    path('destinations/', views.AllDestinations, name='destinations'),
    #path('elogin/', views.loginAdm),
    #path('elogout/', views.logoutAdm),
    
    # everyone
    path('destinations/<int:pk>', views.DestZone, name='destinations_by_zone'),
    path('timetable/<int:did>', views.Show_Timetable),
    path('buy_ticket/<int:tid>', views.Buy_Ticket),

    # #Registered Users
    #path('login/', views.loginPg),
    #path('logout/', views.logoutPg),

    
]