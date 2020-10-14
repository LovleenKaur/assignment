from django.urls import path

from user import views

from rest_framework.authtoken.views import obtain_auth_token

app_name = 'user'

urlpatterns = [
    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('login/', views.CreateTokenView.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('me/', views.ManageUserView.as_view(), name='me'),
]
