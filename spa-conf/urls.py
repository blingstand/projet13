
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('spa/admin/', admin.site.urls),
    path('spa/dashboard', include(("dashboard.urls", 'dashboard'), namespace="dashboard")),
    path('spa/core', include(("core.urls", 'core'), namespace="core")),
    path('spa/mail', include(("mail.urls", 'mail'), namespace="mail")),
    path('spa/sheet', include(("sheet.urls", 'sheet'), namespace="sheet")),
    path('spa/info', include(("info.urls", 'info'), namespace="info")),
    path('spa/user', include(('user.urls', 'user'), namespace="user"))]
