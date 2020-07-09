from django.contrib import admin
from django.urls import path, include


from .views import * 
app_name = 'dashboard' 
urlpatterns = [
    path('', SheetView.as_view(), name='index'),
    path('add', AddSheetView.as_view(), name='add'),
]