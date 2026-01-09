from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model #  importar el modelo de usuario
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404
from django.utils import timezone

# Asegúrate de que tus modelos se llaman así en models.py
from .models import House, Item, Bid 

# ⚠️ IMPORTANTE: Si te da error de "ImportError: cannot import name ItemDetailSerializer",
# borra "ItemDetailSerializer" de aquí abajo y usa "ItemSerializer" en la VISTA 2.
from .serializers import HouseSerializer, ItemSerializer# ItemDetailSerializer
from .serializers import RegisterSerializer # Si haces registro de usuarios


User = get_user_model()

# ==========================================
# VISTA 1: Ver todas las casas
# URL: /api/houses/
# ==========================================
class HouseListAPI(generics.ListAPIView):
    queryset = House.objects.all()
    serializer_class = HouseSerializer
    # OJO: Esto pedirá login. Si quieres que sea público, cambia a [AllowAny]
    permission_classes = [IsAuthenticated] 


# ==========================================
# VISTA 2: Ver detalle de un solo item
# URL: /api/items/<id>/
# ==========================================
class ItemDetailAPI(generics.RetrieveAPIView):
    queryset = Item.objects.all()
    # Si no tienes ItemDetailSerializer en serializers.py, cambia esto por ItemSerializer
    serializer_class = ItemSerializer 
    permission_classes = [AllowAny] # He puesto esto público para que puedas probar fácil


# ==========================================
# VISTA 3: Obtener todos los items (PARA REACT)
# URL: /api/items/
# ==========================================
@api_view(['GET'])
@permission_classes([AllowAny]) # Esto asegura que React pueda leerlo sin login
def get_items(request):
    # ATENCIÓN: Esto busca en la tabla ITEM. 
    # Si guardaste tus fotos en Scene360 y no en Item, esta lista saldrá vacía [].
    items = Item.objects.all() 
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)


# ==========================================
# VISTA 4: Realizar una puja
# URL: /api/items/<id>/bid/
# ==========================================
class PlaceBidAPI(APIView):
    permission_classes = [IsAuthenticated] # Solo usuarios logueados pueden pujar

    def post(self, request, pk):
        # Buscamos el ítem por su ID (pk)
        item = get_object_or_404(Item, pk=pk)
        
        # Obtenemos la cantidad que envían desde el frontend
        bid_amount = request.data.get('amount')

        # 1. Validación: ¿Han enviado dinero?
        if not bid_amount:
            return Response(
                {"error": "Falta la cantidad de la puja"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            amount = float(bid_amount)
        except ValueError:
            return Response(
                {"error": "La cantidad debe ser un número"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2. Validación: Tiempo
        if item.end_time and timezone.now() > item.end_time:
            return Response(
                {"error": "La subasta ha finalizado."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 3. Validación: Vendido
        if item.is_sold:
            return Response(
                {"error": "Este artículo ya está vendido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 4. Validación: Precio
        # Si es la primera puja, debe ser mayor o igual al precio de salida
        current = item.current_price if item.current_price else item.starting_price
        
        if amount <= current:
            return Response(
                {"error": f"Tu puja debe ser mayor que {current}€"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 5. Guardar la puja
        Bid.objects.create(
            item=item,
            user=request.user,
            amount=amount
        )

        # Actualizar el precio del item
        item.current_price = amount
        item.save()

        return Response(
            {"success": "Puja aceptada", "new_price": amount},
            status=status.HTTP_200_OK
        )
        
# ==========================================
# VISTA 5: Registrar nuevo usuario
# URL: /api/register/
# ==========================================
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all() # Necesario para CreateAPIView
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
    