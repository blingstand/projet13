from django.contrib import admin
from django.urls import path, include


from .views import * 
app_name = 'dashboard' 
urlpatterns = [
    path('', MailView.as_view(), name='index'),
    path('cns', CNSView.as_view(), name='cns'),
    path('content', ContentView.as_view(), name='content'),
    path('content/<int:id_mail>', ContentView.as_view(), name='content'),
    path('settings', SettingsView.as_view(), name='settings'),
    path('overview/<int:id_mail>/', OverviewView.as_view(), name='overview'),
    path('overview/', OverviewView.as_view(), name='overview'),
]