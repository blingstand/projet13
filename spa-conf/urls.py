import os 
from django.conf.urls import handler404, handler500
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from django.views.static import serve
from mydashboard.views import MyDashboardView

if os.environ['ENV'] == 'local':
    urlpatterns = [ #online the name is p13
        path('admin/', admin.site.urls),
        path('', include(("user.urls", 'index'), namespace='index')),
        path('mydashboard/', include(("mydashboard.urls", 'mydashboard'), namespace="mydashboard")),
        path('spa_core/', include(("spa_core.urls", 'spa_core'), namespace="spa_core")),
        path('search_bar/', include(("search_bar.urls", 'search_bar'), namespace="search_bar")),
        path('mail/', include(("mail.urls", 'mail'), namespace="mail")),
        path('sheet/', include(("sheet.urls", 'sheet'), namespace="sheet")),
        path('info/', include(("info.urls", 'info'), namespace="info")),
        path('user/', include(('user.urls', 'user'), namespace="user"))]+ \
        static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:  #for heroku the name is spa
    urlpatterns = [
        path('spa/admin/', admin.site.urls),
        path('', include(("user.urls", 'index'), namespace='index')),
        path('spa/mydashboard/', include(("mydashboard.urls", 'mydashboard'), namespace="mydashboard")),
        path('spa/spa_core/', include(("spa_core.urls", 'spa_core'), namespace="spa_core")),
        path('spa/search_bar/', include(("search_bar.urls", 'search_bar'), namespace="search_bar")),
        path('spa/mail/', include(("mail.urls", 'mail'), namespace="mail")),
        path('spa/sheet/', include(("sheet.urls", 'sheet'), namespace="sheet")),
        path('spa/info/', include(("info.urls", 'info'), namespace="info")),
        path('spa/user/', include(('user.urls', 'user'), namespace="user"))]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    if settings.DEBUG:
    	urlpatterns += [
    		url(r'^media/(?P<path>.*)$', serve,{
    			'document_root': settings.MEDIA_ROOT})]

"""Custom 404 and 500 pages works only when Debug is set to false"""
handler404 = MyDashboardView.error_404
handler500 = MyDashboardView.error_500