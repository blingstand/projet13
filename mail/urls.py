""" urls for mail app"""
from django.urls import path

from .views import MailView, CNSView, ContentView, SettingsView, OverviewView
APP_NAME = 'dashboard'

urlpatterns = [
    path('', MailView.as_view(), name='index'),
    path('cns', CNSView.as_view(), name='cns'),
    path('cns/<int:mail_id>', CNSView.as_view(), name='cns'),
    path('content', ContentView.as_view(), name='content'),
    path('content/<int:mail_id>', ContentView.as_view(), name='content'),
    path('content/<int:mail_id>/<str:action>', ContentView.as_view(), name='content'),
    path('settings', SettingsView.as_view(), name='settings'),
    path('settings/<int:mail_id>', SettingsView.as_view(), name='settings'),
    path('overview/<int:mail_id>/', OverviewView.as_view(), name='overview'),
    path('overview/', OverviewView.as_view(), name='overview'),
]
