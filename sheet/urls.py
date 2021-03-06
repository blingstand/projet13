"""script for sheet urls"""
from django.urls import path

from sheet.views import SheetView, AddSheetView, AlterSheetView, \
AddOwnerOpenSheetView, AlterOwnerOpenSheetView, ContactOwnerView,redirect_index

#RETIRÉ AlterOwnerSheetView
APP_NAME = 'sheet'

urlpatterns = [
    path('', redirect_index),
    path('index/', SheetView.as_view(), name='index'),
    path('index/<int:own>', SheetView.as_view(), name='index'),
    path('index/<int:own>/<str:action>/<int:search>', SheetView.as_view(), name='index'),
    #
    path('index/add', AddSheetView.as_view(), name='add'),
    #
    path('index/alter/<int:given_id>', AlterSheetView.as_view(), name='alter'),
    #
    path('index/add_owner_open', AddOwnerOpenSheetView.as_view(), name='add_owner_open'),
    #
    path('index/alter_owner_open/<int:given_id>/', \
        AlterOwnerOpenSheetView.as_view(), name='alter_owner_open'),
    #
    path('index/contact/<int:given_id>', \
        ContactOwnerView.as_view(), name='contact_owner'),
    path('index/contact/<int:given_id>/<str:action>', \
        ContactOwnerView.as_view(), name='contact_owner'),
]
