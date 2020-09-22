from django.contrib import admin
from .models import Sneaker, Purchase, Photo

# Register your models here.
admin.site.register(Sneaker)
admin.site.register(Purchase)
admin.site.register(Photo)
