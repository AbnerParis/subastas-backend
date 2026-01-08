from rest_framework import serializers
from .models import House, Scene360, Item


# =========================
# ITEM – LISTADO / ESCENAS
# =========================
class ItemListSerializer(serializers.ModelSerializer):
    """
    Serializer ligero para mostrar items dentro de escenas 360
    y listados generales.
    """
    class Meta:
        model = Item
        fields = [
            'id',
            'title',
            'current_price',
            'coord_pitch',
            'coord_yaw',
        ]


# =========================
# ITEM – DETALLE COMPLETO
# =========================
class ItemDetailSerializer(serializers.ModelSerializer):
    """
    Serializer completo para el detalle de un item individual.
    """
    class Meta:
        model = Item
        fields = [
            'id',
            'title',
            'description',
            'image',
            'starting_price',
            'current_price',
            'weight_kg',
            'coord_pitch',
            'coord_yaw',
            'auction_end',
            'is_sold',
        ]


# =========================
# ESCENA 360 (CON ITEMS)
# =========================
class Scene360Serializer(serializers.ModelSerializer):
    """
    Escena 360 con sus items incrustados.
    """
    items = ItemListSerializer(many=True, read_only=True)

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
