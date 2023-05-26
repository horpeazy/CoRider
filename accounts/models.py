from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
	MALE = 'male'
	FEMALE = 'female'

	GENDER_CHOICES = [
		(MALE, 'male'),
		(FEMALE, 'female')
	]
	
	username = models.CharField(max_length=255, unique=True)
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	gender = models.CharField(max_length=255, choices=GENDER_CHOICES,  null=True, blank=True)
	profile_picture = models.ImageField(upload_to='uploads/profile-pictures/')
	birthday = models.DateField( null=True, blank=True )
	email = models.EmailField(max_length=255, null=True, blank=True)
	phone_number = models.CharField(max_length=255,  null=True, blank=True)
	address = models.CharField(max_length=500,  null=True, blank=True)
	zip_code = models.CharField(max_length=255,  null=True, blank=True)
	total_rides = models.IntegerField(default=0)
	as_passenger = models.IntegerField(default=0)
	as_driver = models.IntegerField(default=0)
	verified = models.BooleanField(default=False)
	rating = models.DecimalField(default=0.0, decimal_places=1, max_digits=2)
	driver_id = models.CharField(max_length=255, null=True, blank=True)
