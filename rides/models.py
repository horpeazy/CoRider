from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


class Ride(models.Model):
	DRIVER = 'driver'
	PASSENGER = 'passenger'
	ACTIVE = 'started'
	INACTIVE = 'ended'
	PENDING = 'pending'
	
	ROLE_CHOICES = [
		(DRIVER, 'driver'),
		(PASSENGER, 'passenger')
	]
	
	STATUS_CHOICES = [
		(ACTIVE, 'started'),
		(PENDING, 'pending'),
		(INACTIVE, 'ended')
	]

	id = models.AutoField(primary_key=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
	driver = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name="ride_driver")
	passengers = models.ManyToManyField('self', blank=True)
	origin = models.CharField(max_length=500, blank=True, null=True)
	destination = models.CharField(max_length=500, blank=True, null=True)
	origin_lat = models.CharField(max_length=50, blank=True, null=True)
	origin_lon = models.CharField(max_length=50, blank=True, null=True)
	destination_lat = models.CharField(max_length=50, blank=True, null=True)
	destination_lon = models.CharField(max_length=50, blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	route = models.TextField(blank=True, null=True)
	role = models.CharField(max_length=10, choices = ROLE_CHOICES)
	status = models.CharField(max_length=10, choices = STATUS_CHOICES, default="pending")
	
	def __str__(self):
		return f'<from: {self.origin}, to: {self.destination}>'
	

class Review(models.Model):
	id = models.AutoField(primary_key=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="review_owner")
	reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviewer")
	ride = models.ForeignKey(Ride, on_delete=models.CASCADE, related_name="review_ride")
	rating = models.IntegerField(default=0)
	review = models.TextField(blank=False, null=False)
	created_at = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return f'<from: {self.reviewer.username}, to: {self.user.username}>'
	
class Request(models.Model):
	ACCEPTED = 'accepted'
	DECLINED = 'declined'
	PENDING = 'pending'
	
	STATUS_CHOICES = [
		(ACCEPTED, 'accepted'),
		(DECLINED, 'declined'),
		(PENDING, 'pending')
	]

	id = models.AutoField(primary_key=True)
	sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="request_sender")
	receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="request_receiver")
	s_ride = models.ForeignKey(Ride, on_delete=models.CASCADE, related_name="sender_ride")
	r_ride = models.ForeignKey(Ride, on_delete=models.CASCADE, related_name="receiver_ride")
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
	
	def __str__(self):
		return f'<from: {self.sender.username}, to: {self.receiver.username}>'
	
class Rating(models.Model):
	id = models.AutoField(primary_key=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rating_owner")
	rater = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rater")
	ride = models.ForeignKey(Ride, on_delete=models.CASCADE, related_name="rating_ride")
	rate = models.IntegerField(default=0)
	
	def __str__(self):
		return f'<Rater: {self.rate.username}, Rated: {self.user.username}>'


class Vehicle(models.Model):
	id = models.AutoField(primary_key=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="vehicle_owner")
	model = models.CharField(max_length=50, blank=True, null=True)
	make = models.CharField(max_length=50, blank=False, null=False)
	plate_number = models.CharField(max_length=50, blank=False, null=False)
	color = models.CharField(max_length=50, blank=False, null=False)
	
	def __str__(self):
		return f'<owner: {self.user.username}, name: {self.make} {self.model}>'
	

class ContactMessage(models.Model):
	name = models.CharField(max_length=100, blank=False, null=False)
	email = models.EmailField(blank=True, null=True)
	subject = models.CharField(max_length=200)
	message = models.TextField(blank=False, null=False)
	
	def __str__(self):
		return f'message from {self.name} <subject: {self.subject}>'
		
class SubscriptionEmail(models.Model):
	email = models.CharField(max_length=500, blank=False, null=False, unique=True)

	
