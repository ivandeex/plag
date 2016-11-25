"""
PRAG server.
URL Configuration
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('prag.server.urls'))
]

if settings.DEBUG and settings.DEBUG_TOOLBAR_ENABLED:
    import debug_toolbar
    urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls))]
