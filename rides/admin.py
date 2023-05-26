from django.contrib import admin
from django.contrib import admin
from .models import ( Ride, Review, Request,
					  Vehicle, Rating, ContactMessage,
					  SubscriptionEmail )


admin.site.register(( Ride, Review, Request, Vehicle, 
					  Rating, ContactMessage, SubscriptionEmail ))

