
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls import url

from django.views.static import serve

urlpatterns = [
    path('spa/admin/', admin.site.urls),
    path('spa/mydashboard/', include(("mydashboard.urls", 'mydashboard'), namespace="mydashboard")),
    path('spa/core/', include(("core.urls", 'core'), namespace="core")),
    path('spa/mail/', include(("mail.urls", 'mail'), namespace="mail")),
    path('spa/sheet/', include(("sheet.urls", 'sheet'), namespace="sheet")),
    path('spa/info/', include(("info.urls", 'info'), namespace="info")),
    path('spa/user/', include(('user.urls', 'user'), namespace="user"))]

if settings.DEBUG:
	urlpatterns += [
		url(r'^media/(?P<path>.*)$', serve,{
			'document_root': settings.MEDIA_ROOT})]