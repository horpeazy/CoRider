from django.contrib import admin
from django.contrib import admin
from .models import ( Ride, Review, Request,
					  Vehicle, Rating, ContactMessage )

# Register your models here.
admin.site.register(( Ride, Review, Request,
					 Vehicle, Rating, ContactMessage ))

