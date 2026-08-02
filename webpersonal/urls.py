# ==============================================================================
# IMPORTS
# ==============================================================================

from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path

# ==============================================================================
# URLS del proyecto
# ==============================================================================
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    path('', include('core.urls')),
    path('', include('portfolio.urls')),
    path('', include('cv.urls')),
    path('admin/', admin.site.urls),
    prefix_default_language=True
)
