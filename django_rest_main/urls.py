
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    #web applicaation endpoints
    path('students/', include('students.urls')),

    #api endpoints
    path('api/v1/', include('api.urls'))
]
