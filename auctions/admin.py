from django.contrib import admin
from .models import House, Scene360, Item

# Esto hace que aparezcan en tu panel
admin.site.register(House)
admin.site.register(Scene360)
admin.site.register(Item)