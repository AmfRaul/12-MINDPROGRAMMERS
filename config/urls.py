from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", include("dashboard.urls")),

    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),

    path("produtores/", include("produtores.urls")),
    path("marketplace/", include("marketplace.urls")),
    path("pedidos/", include("pedidos.urls")),
    path("avaliacoes/", include("avaliacoes.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
