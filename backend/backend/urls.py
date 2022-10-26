from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

API_URL = 'api/v1'

urlpatterns = [
    path('v-admin/', admin.site.urls),
    path(f'{API_URL}/auth/', include('apps.users.api.urls')),
    path(f'{API_URL}/profile/', include('apps.profiles.api.urls')),
    path(f'{API_URL}/payment/', include('apps.payment.api.urls')),
    path(f'{API_URL}/transcribe/', include('apps.transcribe.api.urls')),
    path(f'{API_URL}/synthesis/', include('apps.synthesis.api.urls')),
    path(f'{API_URL}/chat', include('apps.chat.api.urls')),
]

admin.site.site_header = "Voicen Admin"
admin.site.site_title = "Voicen Admin Portal"
admin.site.index_title = "Welcome to the Voicen Portal"
