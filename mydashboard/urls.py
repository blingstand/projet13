from django.contrib import admin
from django.urls import path, include


from .views import * 
app_name = 'mydashboard' 
urlpatterns = [
    path('', MyDashboardView.as_view(), name='index'),
]


