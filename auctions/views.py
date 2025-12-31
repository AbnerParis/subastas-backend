from rest_framework import generics
from .models import House, Item
from .serializers import HouseSerializer, ItemSerializer
from rest_framework.permissions import IsAuthenticated

# VISTA 1: Ver todas las casas (con sus escenas y objetos dentro)
# URL: /api/houses/
class HouseListAPI(generics.ListAPIView):
    queryset = House.objects.all()
    serializer_class = HouseSerializer
    # ESTA ES LA LÍNEA MÁGICA QUE BLOQUEA EL ACCESO
    permission_classes = [IsAuthenticated]

# VISTA 2: Ver detalle de un solo objeto (para pujar)
# URL: /api/items/5/
class ItemDetailAPI(generics.RetrieveAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer