from django.test import TestCase, Client
from django.urls import reverse
from django.http import JsonResponse
from rides.models import Ride, Rating, Review
from django.contrib.auth import get_user_model
from rides.forms import SubscriptionEmailForm
import json

User = get_user_model()

class FindMatchViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.find_match_url = reverse('api:find_match')
        user = User.objects.create_user(username='testuser', password='testpassword')
        user_2 = User.objects.create_user(username='testuser2', password='testpassword2')
        user.verified = True
        user_2.verified = True
        user_2.profile_picture = 'image.jpg'
        user.save()
        user_2.save()
        self.user = user
        self.user_2 = user_2
    
    def test_find_match_authenticated_user(self):
        self.client.force_login(self.user)
        request_body = {
            'route': [[0.0, 0.0], [1.0, 1.0], [2.0, 2.0]],
            'role': 'driver',
            'destination': 'C',
            'location': 'A',
            'origin_lat': 0.0,
            'origin_lon': 0.0,
            'destination_lat': 1.0,
            'destination_lon': 1.0
        }
        response = self.client.post(self.find_match_url, data=json.dumps(request_body), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('result' in response.json())
        self.assertTrue('id' in response.json())
    
    def test_find_match_unauthenticated_user(self):
        request_body = {
            'route': [[0.0, 0.0], [1.0, 1.0], [2.0, 2.0]],
            'role': 'driver',
            'destination': 'C',
            'location': 'A',
            'origin_lat': 0.0,
            'origin_lon': 0.0,
            'destination_lat': 1.0,
            'destination_lon': 1.0
        }
        response = self.client.post(self.find_match_url, data=json.dumps(request_body), content_type='application/json')
        self.assertEqual(response.status_code, 302)
    
    def test_find_match_invalid_method(self):
        response = self.client.get(self.find_match_url)
        self.assertEqual(response.status_code, 302)
    
    def test_find_match_existing_rides(self):
        self.client.force_login(self.user)
        Ride.objects.create(user=self.user_2, destination='D', origin='A', route=[[0.0, 0.0], [1.0, 1.0], [3.0, 3.0]], role='passenger',
                            origin_lat=0.0, origin_lon=0.0, destination_lat=3.0, destination_lon=3.0)
        request_body = {
            'route': [[0.0, 0.0], [1.0, 1.0], [2.0, 2.0]],
            'role': 'driver',
            'destination': 'C',
            'location': 'A',
            'origin_lat': 0.0,
            'origin_lon': 0.0,
            'destination_lat': 1.0,
            'destination_lon': 1.0
        }
        response = self.client.post(self.find_match_url, data=json.dumps(request_body), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('result' in response.json())
        self.assertTrue('id' in response.json())
        self.assertEqual(len(response.json()['result']), 1)
    
    def test_find_match_no_existing_rides(self):
        self.client.force_login(self.user)
        request_body = {
            'route': [[0.0, 0.0], [1.0, 1.0], [2.0, 2.0]],
            'role': 'driver',
            'destination': 'C',
            'location': 'A',
            'origin_lat': 0.0,
            'origin_lon': 0.0,
            'destination_lat': 1.0,
            'destination_lon': 1.0
        }
        response = self.client.post(self.find_match_url, data=json.dumps(request_body), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('result' in response.json())
        self.assertTrue('id' in response.json())
        self.assertEqual(len(response.json()['result']), 0)

    def test_find_match_invalid_route(self):
    	self.client.force_login(self.user)
    	request_body = {
    	    'route': 'invalid_route',
    	    'role': 'driver',
    	    'destination': 'C',
    	    'location': 'A',
    	    'origin_lat': 0.0,
    	    'origin_lon': 0.0,
    	    'destination_lat': 1.0,
    	    'destination_lon': 1.0
    	}
    	response = self.client.post(self.find_match_url, data=json.dumps(request_body), content_type='application/json')
    	self.assertEqual(response.status_code, 400)

    def test_find_match_insufficient_match_rate(self):
    	self.client.force_login(self.user)
    	Ride.objects.create(user=self.user_2, destination='D', origin='A', route=[[0.0, 0.0], [1.0, 1.0], [3.0, 3.0]], role='passenger',
    	                    origin_lat=0.0, origin_lon=0.0, destination_lat=3.0, destination_lon=3.0)
    	request_body = {
    	    'route': [[0.0, 0.1], [1.2, 1.0], [40.0, 40.0], [50.0, 50.0], [60.0, 60.0], [70.0, 70.0]],
    	    'role': 'driver',
    	    'destination': 'C',
    	    'location': 'A',
    	    'origin_lat': 0.0,
    	    'origin_lon': 0.0,
    	    'destination_lat': 1.0,
    	    'destination_lon': 1.0
    	}
    	response = self.client.post(self.find_match_url, data=json.dumps(request_body), content_type='application/json')
    	self.assertEqual(response.status_code, 200)
    	self.assertTrue('result' in response.json())
    	self.assertTrue('id' in response.json())
    	self.assertEqual(len(response.json()['result']), 0)

    def test_find_match_multiple_matches(self):
    	self.client.force_login(self.user)
    	Ride.objects.create(user=self.user_2, destination='D', origin='A', route=[[0.0, 0.0], [1.0, 1.0], [2.0, 2.0]], role='passenger',
    	                    origin_lat=0.0, origin_lon=0.0, destination_lat=2.0, destination_lon=2.0)
    	Ride.objects.create(user=self.user_2, destination='E', origin='A', route=[[0.0, 0.0], [1.0, 1.0], [3.0, 3.0]], role='passenger',
    	                    origin_lat=0.0, origin_lon=0.0, destination_lat=3.0, destination_lon=3.0)
    	request_body = {
    	    'route': [[0.0, 0.0], [1.0, 1.0], [2.0, 2.0]],
    	    'role': 'driver',
    	    'destination': 'C',
    	    'location': 'A',
    	    'origin_lat': 0.0,
    	    'origin_lon': 0.0,
    	    'destination_lat': 1.0,
    	    'destination_lon': 1.0
    	}
    	response = self.client.post(self.find_match_url, data=json.dumps(request_body), content_type='application/json')
    	self.assertEqual(response.status_code, 200)
    	self.assertTrue('result' in response.json())
    	self.assertTrue('id' in response.json())
    	self.assertEqual(len(response.json()['result']), 2)
    	
    def test_find_match_no_matches(self):
    	self.client.force_login(self.user)
    	request_body = {
        	'route': [[0.0, 0.0], [1.0, 1.0], [2.0, 2.0]],
        	'role': 'driver',
        	'destination': 'C',
        	'location': 'A',
        	'origin_lat': 0.0,
        	'origin_lon': 0.0,
        	'destination_lat': 1.0,
        	'destination_lon': 1.0
    	}
    	response = self.client.post(self.find_match_url, data=json.dumps(request_body), content_type='application/json')
    	self.assertEqual(response.status_code, 200)
    	self.assertTrue('result' in response.json())
    	self.assertTrue('id' in response.json())
    	self.assertEqual(len(response.json()['result']), 0)


class CreateReviewViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.create_review_url = reverse('api:create_review')
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user_2 = User.objects.create_user(username='testuser2', password='testpassword2')
        self.ride = Ride.objects.create(user=self.user_2, destination='D', origin='A')
    
    def test_create_review_authenticated_user(self):
        self.client.force_login(self.user)
        request_body = {
            'review': 'Great ride!',
            'user_id': self.user_2.id,
            'ride_id': self.ride.id,
            'rating': 5
        }
        response = self.client.post(self.create_review_url, data=json.dumps(request_body), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'status': 201, 'message': 'Created Successfully'})
    
    def test_create_review_unauthenticated_user(self):
        request_body = {
            'review': 'Great ride!',
            'user_id': self.user_2.id,
            'ride_id': self.ride.id,
            'rating': 5
        }
        response = self.client.post(self.create_review_url, data=json.dumps(request_body), content_type='application/json')
        self.assertEqual(response.status_code, 302)
    
    def test_create_review_invalid_rating(self):
        self.client.force_login(self.user)
        request_body = {
            'review': 'Great ride!',
            'user_id': self.user_2.id,
            'ride_id': self.ride.id,
            'rating': 'five'
        }
        response = self.client.post(self.create_review_url, data=json.dumps(request_body), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'status': 400, 'message': 'Bad request'})
    
    def test_create_review_missing_rating(self):
        self.client.force_login(self.user)
        request_body = {
            'review': 'Great ride!',
            'user_id': self.user_2.id,
            'ride_id': self.ride.id
        }
        response = self.client.post(self.create_review_url, data=json.dumps(request_body), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'status': 201, 'message': 'Created Successfully'})
    
    def test_create_review_no_review(self):
        self.client.force_login(self.user)
        request_body = {
            'user_id': self.user_2.id,
            'ride_id': self.ride.id,
            'rating': 5
        }
        response = self.client.post(self.create_review_url, data=json.dumps(request_body), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'status': 201, 'message': 'Created Successfully'})
    
    def test_create_review_existing_rating(self):
        self.client.force_login(self.user)
        Rating.objects.create(user=self.user_2, rate=4, rater=self.user, ride=self.ride)
        request_body = {
            'review': 'Great ride!',
            'user_id': self.user_2.id,
            'ride_id': self.ride.id,
            'rating': 5
        }
        response = self.client.post(self.create_review_url, data=json.dumps(request_body), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'status': 201, 'message': 'Created Successfully'})
    
    def test_create_review_no_existing_rating(self):
        self.client.force_login(self.user)
        request_body = {
            'review': 'Great ride!',
            'user_id': self.user_2.id,
            'ride_id': self.ride.id,
            'rating': 5
        }
        response = self.client.post(self.create_review_url, data=json.dumps(request_body), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'status': 201, 'message': 'Created Successfully'})
    
    def test_create_review_multiple_reviews(self):
        self.client.force_login(self.user)
        Review.objects.create(user=self.user_2, review='Good ride!', rating=4, reviewer=self.user, ride=self.ride)
        request_body = {
            'review': 'Great ride!',
            'user_id': self.user_2.id,
            'ride_id': self.ride.id,
            'rating': 5
        }
        response = self.client.post(self.create_review_url, data=json.dumps(request_body), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'status': 201, 'message': 'Created Successfully'})
    
    def test_create_review_invalid_method(self):
        response = self.client.get(self.create_review_url)
        self.assertEqual(response.status_code, 302)


class EmailSubscriptionViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.email_subscription_url = reverse('api:email_subscription')
    
    def test_email_subscription_valid_data(self):
        request_body = {
            'email': 'test@example.com'
        }
        response = self.client.post(self.email_subscription_url, data=json.dumps(request_body), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'status': 201, 'message': 'Created Successfully'})
    
    def test_email_subscription_invalid_data(self):
        request_body = {
            'email': 'invalid-email'
        }
        response = self.client.post(self.email_subscription_url, data=json.dumps(request_body), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'status': 400, 'message': 'Invalid request'})
    
    def test_email_subscription_missing_field(self):
        request_body = {}
        response = self.client.post(self.email_subscription_url, data=json.dumps(request_body), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'status': 400, 'message': 'Invalid request'})
    
    def test_email_subscription_invalid_method(self):
        response = self.client.get(self.email_subscription_url)
        self.assertEqual(response.status_code, 405)
    
    def test_email_subscription_form_valid(self):
        request_body = {
            'email': 'test@example.com'
        }
        form = SubscriptionEmailForm(request_body)
        self.assertTrue(form.is_valid())
    
    def test_email_subscription_form_invalid(self):
        request_body = {
            'email': 'invalid-email'
        }
        form = SubscriptionEmailForm(request_body)
        self.assertFalse(form.is_valid())
    
    def test_email_subscription_form_missing_field(self):
        request_body = {}
        form = SubscriptionEmailForm(request_body)
        self.assertFalse(form.is_valid())


