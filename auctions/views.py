from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import House, Item, Bid, Scene360
from .serializers import HouseSerializer, ItemDetailSerializer
from .serializers import ItemSerializer


# VISTA 1: Ver todas las casas (requiere autenticación)
# URL: /api/houses/
class HouseListAPI(generics.ListAPIView):
    queryset = House.objects.all()
    serializer_class = HouseSerializer
    permission_classes = [IsAuthenticated]


# VISTA 2: Ver detalle de un solo item
# URL: /api/items/<id>/
class ItemDetailAPI(generics.RetrieveAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemDetailSerializer


# VISTA 3: Obtener todos los items (SIN autenticación)
# URL: /api/items/
@api_view(['GET'])
def get_items(request):
    items = Item.objects.all()
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)


# VISTA 4: Realizar una puja (requiere autenticación)
# URL: /api/items/<id>/bid/
class PlaceBidAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        bid_amount = request.data.get('amount')

        if not bid_amount:
            return Response(
                {"error": "Falta la cantidad"},
                status=status.HTTP_400_BAD_REQUEST
            )

        amount = float(bid_amount)

        # Validación de tiempo de subasta
        if timezone.now() > item.auction_end:
            return Response(
                {"error": "La subasta ha finalizado, ya no se admiten pujas."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if item.is_sold:
            return Response(
                {"error": "Este artículo ya se ha vendido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if amount <= item.current_price:
            return Response(
                {"error": f"Tu puja debe ser mayor que {item.current_price}€"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Guardar puja
        Bid.objects.create(
            item=item,
            user=request.user,
            amount=amount
        )

        item.current_price = amount
        item.save()

        return Response(
            {"success": "Puja aceptada", "new_price": amount},
            status=status.HTTP_200_OK
        )
