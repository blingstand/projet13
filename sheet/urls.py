from django.contrib import admin
from django.urls import path, include


from .views import * 
app_name = 'dashboard' 
urlpatterns = [
    path('', SheetView.as_view(), name='index'),
    path('add', AddSheetView.as_view(), name='add'),
    path('alter/<int:given_id>', AlterSheetView.as_view(), name='alter'),
    path('alter_owner/<int:given_id>', AlterOwnerSheetView.as_view(), name='alter_owner'),
]