from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('default/', include('django.contrib.flatpages.urls')),
    path('', include('NewsPortal.urls')),
    path('sign/', include('Sign.urls')),
    path('accounts/', include('allauth.urls')),
]
