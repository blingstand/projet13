from django.contrib import admin
from django.urls import path, include


from .views import * 
app_name = 'dashboard' 
urlpatterns = [
    path('', InfosView.as_view(), name='index'),
    path('legal_notice', LegalNoticeView.as_view(), name='legal_notice'),
]