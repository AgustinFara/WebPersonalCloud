# ==============================================================================
# IMPORTS
# ==============================================================================

from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings



# ==============================================================================
# URLS del proyecto
# ==============================================================================

urlpatterns = [
    path('', include('core.urls')),
    path('', include('portfolio.urls')),
    path('', include('cv.urls')),
    path('admin/', admin.site.urls),
]


