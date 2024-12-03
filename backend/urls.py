# Project Routing URL
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static 
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('users.urls')),  # Correctly include the users app's urls
    path('api/products/',include('products.urls')),
    path('api/payments/',include('payments.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)