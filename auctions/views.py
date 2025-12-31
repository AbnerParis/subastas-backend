from rest_framework import generics
from .models import House, Item
from .serializers import HouseSerializer, ItemSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Item, Bid
from django.utils import timezone  # <--- IMPORTANTE

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
    
class PlaceBidAPI(APIView):
    permission_classes = [IsAuthenticated] # Solo usuarios registrados

    def post(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        bid_amount = request.data.get('amount')
        
        if not bid_amount:
            return Response({"error": "Falta la cantidad"}, status=status.HTTP_400_BAD_REQUEST)
        
        amount = float(bid_amount)

        # --- BLOQUE NUEVO: VALIDACIÓN DE TIEMPO ---
        # Si la fecha actual (now) es MAYOR que el fin de la subasta...
        if timezone.now() > item.auction_end:
            return Response(
                {"error": "La subasta ha finalizado, ya no se admiten pujas."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        # ------------------------------------------

        if item.is_sold:
             return Response({"error": "Este artículo ya se ha vendido"}, status=status.HTTP_400_BAD_REQUEST)

        if amount <= item.current_price:
            return Response(
                {"error": f"Tu puja debe ser mayor que {item.current_price}€"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # ... (El resto del código de guardar la puja sigue igual) ...
        Bid.objects.create(item=item, user=request.user, amount=amount)
        item.current_price = amount
        item.save()
        
        return Response({"success": "Puja aceptada", "new_price": amount}, status=status.HTTP_200_OK)