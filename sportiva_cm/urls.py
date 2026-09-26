from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import profiles_list_view

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('profiles/', profiles_list_view, name='profiles_list'),
    path('organizations/', include('organizations.urls')),
    path('events/', include('events.urls')),
    path('media-feed/', include('media_feed.urls')),
    path('marketplace/', include('marketplace.urls')),
    path('sponsorships/', include('sponsorships.urls')),
    path('chat/', include('chat.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
