from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/', include('users.urls', namespace='api_users')),
    path('admin/', admin.site.urls),
    path("materials/", include('materials.urls', namespace='materials')),
    path("users/", include('users.urls', namespace='users')),
]
