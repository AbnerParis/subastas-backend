"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from auctions.views import get_items
# Importamos tus vistas
from auctions.views import HouseListAPI, ItemDetailAPI
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from auctions.views import HouseListAPI, ItemDetailAPI, PlaceBidAPI  # <--- Añade PlaceBidAPI
from auctions.views import get_items, RegisterView #<--- Añade RegisterView


urlpatterns = [
    path('admin/', admin.site.urls),
    
    # --- TUS ENDPOINTS (ENCHUFES) ---
  path('api/houses/', HouseListAPI.as_view(), name='house-list'),
    path('api/items/<int:pk>/', ItemDetailAPI.as_view(), name='item-detail'),
    path('api/items/', get_items, name='get_items'), # <--- Ruta para obtener todos los items
    # --- 2. AÑADE ESTAS RUTAS DE LOGIN ---
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # El Login
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # Renovar tarjeta
    path('api/items/<int:pk>/bid/', PlaceBidAPI.as_view(), name='place-bid'), # <--- Ruta para pujar
    path('api/items/', get_items, name='get_items'),
    path('api/register/', RegisterView.as_view(), name='register'), #<--- Ruta para registrar nuevo usuario
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)