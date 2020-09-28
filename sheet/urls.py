from django.contrib import admin
from django.urls import path, include


from .views import * 
app_name = 'sheet' 
urlpatterns = [
    path('', redirectIndex),
    path('index/', SheetView.as_view(), name='index'),
    path('index/<int:own>', SheetView.as_view(), name='index'),
    path('index/add', AddSheetView.as_view(), name='add'),
    path('index/alter/<int:given_id>', AlterSheetView.as_view(), name='alter'),
    path('index/alter_owner/<int:given_id>', AlterOwnerSheetView.as_view(), name='alter_owner'),
    path('index/alter_owner/<int:given_id>/<str:action>', AlterOwnerSheetView.as_view(), name='alter_owner'),
    path('index/add_owner', AddOwnerSheetView.as_view(), name='add_owner'),
    path('index/contact/<int:given_id>', ContactOwnerView.as_view(), name='contact_owner'),
    path('index/contact/<int:given_id>/<str:action>', ContactOwnerView.as_view(), name='contact_owner'),
]