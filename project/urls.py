from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.conf import settings
from rest_framework_swagger.views import get_swagger_view


schema_view = get_swagger_view(title='Django osw4l docker api v1')

urlpatterns = [
    path('', schema_view),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

