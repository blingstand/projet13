from django.contrib import admin
from django.urls import path, include


from .views import * 
app_name = 'dashboard' 
urlpatterns = [
    path('', SheetView.as_view(), name='index'),
]