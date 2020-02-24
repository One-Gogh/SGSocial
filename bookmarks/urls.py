from django.contrib import admin
from django.urls import path, include
from account.views import feed
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	path('', feed, name='feed'),

    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('images/', include(('images.urls', 'images'), namespace='images')),
]
if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
