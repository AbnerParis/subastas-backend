from rest_framework import serializers
from .models import House, Scene360, Item

# 1. Serializer del Objeto (El nivel más bajo)
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = [
            'id', 'title', 'description', 
            'starting_price', 'current_price', 'weight_kg',
            'coord_pitch', 'coord_yaw', 
            'auction_end', 'is_sold'
        ]

# 2. Serializer de la Escena (Incluye los objetos dentro)
class Scene360Serializer(serializers.ModelSerializer):
    # Esto es la magia: Incrustamos los items dentro de la escena
    items = ItemSerializer(many=True, read_only=True)

    class Meta:
        model = Scene360
        fields = ['id', 'name', 'image', 'items']

# 3. Serializer de la Casa (Incluye las escenas dentro)
class HouseSerializer(serializers.ModelSerializer):
    # Incrustamos las escenas dentro de la casa
    scenes = Scene360Serializer(many=True, read_only=True)

    class Meta:
        model = House
        fields = ['id', 'title', 'address', 'created_at', 'scenes']
        
# 4. Serializer detallado del Objeto (con imagen)        
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = [
            'id', 'title', 'description', 'image', # <--- AÑADE 'image' AQUÍ
            'starting_price', 'current_price', # ... resto de campos
        ]