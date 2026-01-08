from rest_framework import serializers
# ⚠️ IMPORTANTE: Asegúrate de que en models.py existen estas 3 clases (House, Scene360, Item)
from .models import House, Scene360, Item 

# =========================
# ITEM – SERIALIZER PRINCIPAL
# =========================
class ItemSerializer(serializers.ModelSerializer):
    """
    Este es el que busca tu views.py. 
    Contiene toda la info del Item.
    """
    class Meta:
        model = Item
        fields = '__all__'  # Truco: Trae todos los campos automáticamente


# =========================
# ESCENA 360 (CON ITEMS)
# =========================
class Scene360Serializer(serializers.ModelSerializer):
    """
    Escena 360 con sus items incrustados.
    """
    # Usamos el ItemSerializer para mostrar los objetos dentro de la escena
    items = ItemSerializer(many=True, read_only=True)

    class Meta:
        model = Scene360
        fields = [
            'id',
            'name',
            'image',
            'items',
        ]


# =========================
# CASA (CON ESCENAS)
# =========================
class HouseSerializer(serializers.ModelSerializer):
    """
    Casa con todas sus escenas 360.
    """
    scenes = Scene360Serializer(many=True, read_only=True)

    class Meta:
        model = House
        fields = [
            'id',
            'title',
            'address',
            'created_at',
            'scenes',
        ]