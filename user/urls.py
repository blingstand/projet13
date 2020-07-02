from django.contrib import admin
from django.urls import path, include

#from current app
from .views import ConnectionView, RegisterView

app_name = 'user'
urlpatterns = [
    path('', ConnectionView.as_view()),
    path('connection', ConnectionView.as_view(), name="connection"),
    path('register', RegisterView.as_view(), name="register"),

]
