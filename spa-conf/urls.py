
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('spa/admin/', admin.site.urls),
    path('spa/dashboard', include(("dashboard.urls", 'dashboard'), namespace="dashboard")),
    path('spa/core', include(("core.urls", 'core'), namespace="core")),
    path('spa/user', include(('user.urls', 'user'), namespace="user"))]
