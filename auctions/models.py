from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.conf import settings

class House(models.Model):
    title = models.CharField(max_length=200) # Ej: Piso en Calle Serrano
    address = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Scene360(models.Model):
    house = models.ForeignKey(House, related_name='scenes', on_delete=models.CASCADE)
    name = models.CharField(max_length=100) # Ej: Salón Principal
    image = models.ImageField(upload_to='scenes/') # Aquí va la foto de la Ricoh

    def __str__(self):
        return f"{self.name} - {self.house.title}"

class Item(models.Model):
    scene = models.ForeignKey(Scene360, related_name='items', on_delete=models.CASCADE)
    title = models.CharField(max_length=200) # Ej: Lámpara Antigua
    description = models.TextField(blank=True)
    # upload_to='items/': Crea una carpeta "items" dentro del Bucket S3
    image = models.ImageField(upload_to='items/', null=True, blank=True) 
    #
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    weight_kg = models.FloatField(default=0, help_text="Peso aproximado en Kg para el envío")
    
    # Coordenadas para el punto en el 3D (Pitch/Yaw)
    coord_pitch = models.FloatField(help_text="Coordenada Vertical en la foto 360")
    coord_yaw = models.FloatField(help_text="Coordenada Horizontal en la foto 360")
    
    
    #end time: Fecha y hora en la que termina la subasta
    # Si no se pone, se calcula automáticamente a los 3 días de crear el ítem
    # Si quieres poner una fecha personalizada:  
    #  item.end_time = timezone.now() + timedelta(hours=24)
    end_time = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Si es nuevo, ponemos el precio actual igual al de salida
        if not self.id:
            self.current_price = self.starting_price
            # La subasta dura 3 días desde que se crea
            self.auction_end = timezone.now() + timedelta(days=3)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
class Bid(models.Model):
    item = models.ForeignKey(Item, related_name='bids', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='bids', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount}€ en {self.item.title}"