# dockerfile for corider image
FROM python:slim

WORKDIR /corider
COPY . .

RUN pip install -r requirements.txt
RUN python manage.py collectstatic --noinput

EXPOSE 8000


using the format below

"""
from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from rides.forms import ContactMessageForm
from rides.models import ContactMessage
from rides.views import ( home, about, contact, )

class HomeViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()

    def test_view_returns_200_status_code(self):
        request = self.factory.get(reverse('rides:home'))
        response = home(request)
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('rides:home'))
        self.assertTemplateUsed(response, 'rides/home.html')

    def test_view_does_not_require_authentication(self):
        request = self.factory.get(reverse('rides:home'))
        response = home(request)
        self.assertFalse(response.has_header('WWW-Authenticate'))

    def test_view_does_not_raise_exception(self):
        request = self.factory.get(reverse('rides:home'))
        try:
            response = home(request)
        except Exception as e:
            self.fail(f"The view raised an exception: {e}")


class AboutViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        
    def test_view_returns_200_status_code(self):
        request = self.factory.get(reverse('rides:about'))
        response = about(request)
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('rides:about'))
        self.assertTemplateUsed(response, 'rides/about.html')

    def test_view_does_not_require_authentication(self):
        request = self.factory.get(reverse('rides:about'))
        response = about(request)
        self.assertFalse(response.has_header('WWW-Authenticate'))
        
    def test_view_does_not_raise_exception(self):
        request = self.factory.get(reverse('rides:about'))
        try:
            response = about(request)
        except Exception as e:
            self.fail(f"The view raised an exception: {e}")


class ContactViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('rides:contact'))
        self.assertTemplateUsed(response, 'rides/contact.html')

    def test_view_contains_title_in_context(self):
        response = self.client.get(reverse('rides:contact'))
        self.assertEqual(response.context['title'], 'Contact')

    def test_view_contains_form_in_context(self):
        response = self.client.get(reverse('rides:contact'))
        self.assertIsInstance(response.context['form'], ContactMessageForm)

    def test_view_does_not_save_invalid_form_on_post(self):
        form_data = {
            'name': 'John Doe',
            'email': 'invalid_email',  # Invalid email format
            'message': 'Hello, I have a question.'
        }
        response = self.client.post(reverse('rides:contact'), data=form_data)
        self.assertEqual(ContactMessage.objects.count(), 0)

    def test_view_does_not_save_form_on_get_request(self):
        response = self.client.get(reverse('rides:contact'))
        self.assertEqual(ContactMessage.objects.count(), 0)

    def test_view_uses_correct_form_template(self):
        response = self.client.get(reverse('rides:contact'))
        self.assertTemplateUsed(response, 'rides/contact.html')

"""

This is the models.py file

"""
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

	
	"""

write a test for this view, at leat 10, the actual python code

@login_required
def match(request):
	ride_id = request.GET.get('ride_id', None)
	match_id = request.GET.get('match_id', None)
	role = request.GET.get('role', None)
	ride = Ride.objects.filter(id=ride_id).first()
	match = Ride.objects.filter(id=match_id).first()
	req = Request.objects.\
				  filter(sender=match.user, receiver=ride.user,s_ride=match).\
				  first()
	if ride and match:
		if role == 'passenger':
			ride.driver = match
			match.passengers.add(ride)
		else:
			ride.passengers.add(match)
			match.driver = ride
		req.status = Request.ACCEPTED
		if ride.status == Ride.PENDING:
			ride.status = Ride.ACTIVE
		if match.status == Ride.PENDING:
			match.status = Ride.ACTIVE
		ride.save()
		match.save()
		req.save()
		return redirect('rides:ride_detail', ride_id=ride_id)  
	else:
		return render(request, 'rides/404.html', context)
		
		
		
