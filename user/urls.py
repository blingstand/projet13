from django.contrib import admin
from django.urls import path, include

#from current app
from .views import *

app_name = 'user'
urlpatterns = [
    path('', ConnectionView.as_view()),
    path('connection', ConnectionView.as_view(), name="connection"),
    path('logout', LogoutView.as_view(), name="logout"),

]
