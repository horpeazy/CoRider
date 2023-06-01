from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from rides.forms import ContactMessageForm, VehicleForm
from accounts.forms import EditAccountForm
from rides.models import ( ContactMessage, Ride, Review,
						   Vehicle, Rating, Request )
from rides.views import ( home, about, contact, 
						  team, rides, reviews,
						  profile_reviews, account,
						  edit_account, ride_detail,
						  match, decline, request, end_trip )


User = get_user_model()


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


class TeamViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_view_returns_200_status_code(self):
        response = self.client.get(reverse('rides:team'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('rides:team'))
        self.assertTemplateUsed(response, 'rides/team.html')

    def test_view_does_not_require_authentication(self):
        response = self.client.get(reverse('rides:team'))
        self.assertFalse(response.has_header('WWW-Authenticate'))

    def test_view_does_not_raise_exception(self):
        response = self.client.get(reverse('rides:team'))
        self.assertNotEqual(response.status_code, 500)
        

class ServicesViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_view_returns_200_status_code(self):
        response = self.client.get(reverse('rides:services'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('rides:services'))
        self.assertTemplateUsed(response, 'rides/services.html')

    def test_view_does_not_require_authentication(self):
        response = self.client.get(reverse('rides:services'))
        self.assertFalse(response.has_header('WWW-Authenticate'))

    def test_view_does_not_raise_exception(self):
        response = self.client.get(reverse('rides:services'))
        self.assertNotEqual(response.status_code, 500)
        
        
class TermsViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_view_returns_200_status_code(self):
        response = self.client.get(reverse('rides:terms'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('rides:terms'))
        self.assertTemplateUsed(response, 'rides/terms.html')

    def test_view_does_not_require_authentication(self):
        response = self.client.get(reverse('rides:terms'))
        self.assertFalse(response.has_header('WWW-Authenticate'))

    def test_view_does_not_raise_exception(self):
        response = self.client.get(reverse('rides:terms'))
        self.assertNotEqual(response.status_code, 500)
        
        
class PrivacyViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_view_returns_200_status_code(self):
        response = self.client.get(reverse('rides:privacy'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('rides:privacy'))
        self.assertTemplateUsed(response, 'rides/privacy.html')

    def test_view_does_not_require_authentication(self):
        response = self.client.get(reverse('rides:privacy'))
        self.assertFalse(response.has_header('WWW-Authenticate'))

    def test_view_does_not_raise_exception(self):
        response = self.client.get(reverse('rides:privacy'))
        self.assertNotEqual(response.status_code, 500)
        
class RideViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.user = user

    def test_view_returns_200_status_code(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('rides:ride'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('rides:ride'))
        self.assertTemplateUsed(response, 'rides/ride.html')

    def test_view_requires_authentication(self):
        response = self.client.get(reverse('rides:ride'))
        self.assertEqual(response.status_code, 302)

    def test_view_does_not_raise_exception(self):
        response = self.client.get(reverse('rides:ride'))
        self.assertNotEqual(response.status_code, 500)


class RidesViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        user = User.objects.create_user(username='testuser', password='testpassword')
        user_2 = User.objects.create_user(username='testuser2', password='testpassword2')
        user.verified = True
        user_2.verified = True
        user_2.profile_picture = 'image.jpg'
        user.save()
        user_2.save()
        self.user = user
        self.user_2 = user_2

    def test_view_returns_200_status_code(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('rides:rides'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('rides:rides'))
        self.assertTemplateUsed(response, 'rides/rides.html')

    def test_view_requires_authentication(self):
        response = self.client.get(reverse('rides:rides'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/accounts/login/?next=/rides/')

    def test_view_does_not_raise_exception(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('rides:rides'))
        self.assertNotEqual(response.status_code, 500)

    def test_view_contains_title_in_context(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('rides:rides'))
        self.assertEqual(response.context['title'], 'Rides')

    def test_view_returns_404_for_invalid_url(self):
        self.client.force_login(self.user)
        response = self.client.get('/rides/invalid_url/')
        self.assertEqual(response.status_code, 404)

    def test_view_uses_correct_form_template(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('rides:rides'))
        self.assertTemplateUsed(response, 'rides/rides.html')


class ReviewsViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_view_returns_200_status_code(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('rides:reviews'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('rides:reviews'))
        self.assertTemplateUsed(response, 'rides/reviews.html')

    def test_view_requires_authentication(self):
        response = self.client.get(reverse('rides:reviews'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/accounts/login/?next=/reviews/')

    def test_view_does_not_raise_exception(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('rides:reviews'))
        self.assertNotEqual(response.status_code, 500)

    def test_view_returns_404_for_invalid_url(self):
        self.client.force_login(self.user)
        response = self.client.get('/reviews/invalid_url/')
        self.assertEqual(response.status_code, 404)


    def test_view_uses_correct_form_template(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('rides:reviews'))
        self.assertTemplateUsed(response, 'rides/reviews.html')


class ProfileReviewsViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_view_returns_200_status_code(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('rides:profile_reviews', args=['testuser']))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('rides:profile_reviews', args=['testuser']))
        self.assertTemplateUsed(response, 'rides/reviews.html')

    def test_view_requires_authentication(self):
        response = self.client.get(reverse('rides:profile_reviews', args=['testuser']))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/accounts/login/?next=/reviews/testuser')

    def test_view_does_not_raise_exception(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('rides:profile_reviews', args=['testuser']))
        self.assertNotEqual(response.status_code, 500)

    def test_view_contains_title_in_context(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('rides:profile_reviews', args=['testuser']))
        self.assertEqual(response.context['title'], 'Profile Reviews')

    def test_view_returns_404_for_invalid_user(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('rides:profile_reviews', args=['invaliduser']))
        self.assertEqual(response.status_code, 302)

    def test_view_returns_404_for_nonexistent_user(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('rides:profile_reviews', args=['nonexistentuser']))
        self.assertEqual(response.status_code, 302)

    def test_view_uses_correct_form_template(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('rides:profile_reviews', args=['testuser']))
        self.assertTemplateUsed(response, 'rides/reviews.html')


class AccountViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        user = User.objects.create_user(username='testuser', password='testpassword')
        user_2 = User.objects.create_user(username='testuser2', password='testpassword2')
        user.verified = True
        user_2.verified = True
        user_2.profile_picture = 'image.jpg'
        user.save()
        user_2.save()
        self.user = user
        self.user_2 = user_2
        self.s_ride = Ride.objects.create(user=self.user, destination='D', origin='A', route=[[0.0, 0.0], [1.0, 1.0], [3.0, 3.0]], role='passenger',
                         origin_lat=0.0, origin_lon=0.0, destination_lat=3.0, destination_lon=3.0)
        self.r_ride = Ride.objects.create(user=self.user_2, destination='D', origin='A', route=[[0.0, 0.0], [1.0, 1.0], [3.0, 3.0]], role='driver',
                         origin_lat=0.0, origin_lon=0.0, destination_lat=3.0, destination_lon=3.0)
        self.vehicle = Vehicle.objects.create(user=self.user, make='Toyota', model='Corolla', plate_number='123', color='red')
        self.rating = Rating.objects.create(user=self.user, rate=4, rater=self.user_2, ride=self.s_ride)
        self.request = Request.objects.create(sender=self.user, receiver=self.user, s_ride=self.s_ride, r_ride=self.r_ride, status=Request.ACCEPTED)

    def test_view_returns_200_status_code(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('rides:account'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('rides:account'))
        self.assertTemplateUsed(response, 'rides/account.html')

    def test_view_requires_authentication(self):
        response = self.client.get(reverse('rides:account'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/accounts/login/?next=/account/')

    def test_view_does_not_raise_exception(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('rides:account'))
        self.assertNotEqual(response.status_code, 500)

    def test_view_contains_title_in_context(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('rides:account'))
        self.assertEqual(response.context['title'], 'Account Information')

    def test_view_contains_user_in_context(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('rides:account'))
        self.assertEqual(response.context['user'], self.user)

    def test_view_contains_vehicle_in_context(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('rides:account'))
        self.assertEqual(response.context['vehicle'], self.vehicle)

    def test_view_calculates_user_availability(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('rides:account'))
        user = response.context['user']
        self.assertEqual(user.availability, 100)

    def test_view_uses_correct_form_template(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('rides:account'))
        self.assertTemplateUsed(response, 'rides/account.html')


class EditAccountViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.vehicle = Vehicle.objects.create(user=self.user, make='Toyota', model='Corolla', color='red', plate_number='3272')

    def test_view_returns_200_status_code(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('rides:edit_account'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('rides:edit_account'))
        self.assertTemplateUsed(response, 'rides/edit-account.html')

    def test_view_requires_authentication(self):
        response = self.client.get(reverse('rides:edit_account'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/accounts/login/?next=/account/edit')

    def test_view_does_not_raise_exception(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('rides:edit_account'))
        self.assertNotEqual(response.status_code, 500)

    def test_view_contains_account_form_in_context(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('rides:edit_account'))
        self.assertIsInstance(response.context['account_form'], EditAccountForm)

    def test_view_contains_vehicle_form_in_context(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('rides:edit_account'))
        self.assertIsInstance(response.context['vehicle_form'], VehicleForm)


    def test_view_redirects_to_account_after_successful_update(self):
        self.client.force_login(self.user)
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
        }
        response = self.client.post(reverse('rides:edit_account'), data=form_data)
        self.assertEqual(response.status_code, 200)

    def test_view_does_not_save_invalid_form_on_post(self):
        self.client.force_login(self.user)
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'invalid_email',
        }
        response = self.client.post(reverse('rides:edit_account'), data=form_data)
        self.user.refresh_from_db()
        self.assertNotEqual(self.user.email, 'invalid_email')


class ProfileViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.vehicle = Vehicle.objects.create(user=self.user, make='Toyota', model='Corolla')

    def test_view_returns_200_status_code(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('rides:profile', args=['testuser']))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('rides:profile', args=['testuser']))
        self.assertTemplateUsed(response, 'rides/profile.html')

    def test_view_requires_authentication(self):
        response = self.client.get(reverse('rides:profile', args=['testuser']))
        self.assertEqual(response.status_code, 302)

    def test_view_does_not_raise_exception(self):
        response = self.client.get(reverse('rides:profile', args=['testuser']))
        self.assertNotEqual(response.status_code, 500)

    def test_view_redirects_to_404_for_nonexistent_user(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('rides:profile', args=['nonexistentuser']))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/404/')


class RideDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.ride = Ride.objects.create(user=self.user, role=Ride.PASSENGER, status=Ride.ACTIVE)

    def test_view_returns_200_status_code(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('rides:ride_detail', args=[self.ride.id]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('rides:ride_detail', args=[self.ride.id]))
        self.assertTemplateUsed(response, 'rides/ride-detail.html')

    def test_view_requires_authentication(self):
        response = self.client.get(reverse('rides:ride_detail', args=[self.ride.id]))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_view_redirects_to_404_for_nonexistent_ride(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('rides:ride_detail', args=[999]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/404/')

    def test_view_contains_ride_in_context(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('rides:ride_detail', args=[self.ride.id]))
        self.assertEqual(response.context['ride']['user_id'], self.user.id)

    def test_view_contains_matches_in_context(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('rides:ride_detail', args=[self.ride.id]))
        self.assertEqual(response.context['matches'], [])

    def test_view_does_not_match_invalid_routes(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('rides:ride_detail', args=[self.ride.id]))
        self.assertEqual(len(response.context['matches']), 0)


class MatchViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user1 = User.objects.create_user(username='user1', password='testpassword1')
        self.user2 = User.objects.create_user(username='user2', password='testpassword2')
        ride = Ride.objects.create(user=self.user1, destination='D', origin='A', route=[[0.0, 0.0], [1.0, 1.0], [3.0, 3.0]], role='passenger',
                            origin_lat=0.0, origin_lon=0.0, destination_lat=3.0, destination_lon=3.0)
        ride.save()
        self.ride = ride
        match = Ride.objects.create(user=self.user2, destination='D', origin='A', route=[[0.0, 0.0], [1.0, 1.0], [3.0, 3.0]], role='driver',
                            origin_lat=0.0, origin_lon=0.0, destination_lat=3.0, destination_lon=3.0)
        match.save()
        self.match = match
        self.request = Request.objects.create(sender=self.user2, receiver=self.user1, s_ride=self.match, r_ride=self.ride)

    def test_view_matches_ride_with_passenger_role(self):
        request = self.factory.get(reverse('rides:match'), {'ride_id': self.ride.id, 'match_id': self.match.id, 'role': 'passenger'})
        request.user = self.user1
        response = match(request)
        self.assertEqual(response.status_code, 302)
        self.ride.refresh_from_db()
        self.match.refresh_from_db()
        self.request.refresh_from_db()
        self.assertEqual(self.ride.driver, self.match)
        self.assertIn(self.ride, self.match.passengers.all())
        self.assertEqual(self.request.status, Request.ACCEPTED)
        self.assertEqual(self.ride.status, Ride.ACTIVE)
        self.assertEqual(self.match.status, Ride.ACTIVE)

    def test_view_matches_ride_with_driver_role(self):
        request = self.factory.get(reverse('rides:match'), {'ride_id': self.ride.id, 'match_id': self.match.id, 'role': 'driver'})
        request.user = self.user1
        response = match(request)
        self.assertEqual(response.status_code, 302)
        self.ride.refresh_from_db()
        self.match.refresh_from_db()
        self.request.refresh_from_db()
        self.assertIn(self.match, self.ride.passengers.all())
        self.assertEqual(self.match.driver, self.ride)
        self.assertEqual(self.request.status, Request.ACCEPTED)
        self.assertEqual(self.ride.status, Ride.ACTIVE)
        self.assertEqual(self.match.status, Ride.ACTIVE)

    def test_view_returns_302_for_invalid_role(self):
        self.client.force_login(self.user1)
        request = self.factory.get(reverse('rides:match'), {'ride_id': self.ride.id, 'match_id': self.match.id, 'role': 'invalid'})
        request.user = self.user1
        response = match(request)
        self.assertEqual(response.status_code, 302)
        self.ride.refresh_from_db()
        self.match.refresh_from_db()
        self.request.refresh_from_db()
        self.assertIsNone(self.ride.driver)
        self.assertEqual(self.request.status, Request.ACCEPTED)
        self.assertEqual(self.ride.status, Ride.ACTIVE)
        self.assertEqual(self.match.status, Ride.ACTIVE)

    def test_view_requires_authentication(self):
        response = self.client.get(reverse('rides:match'))
        self.assertEqual(response.status_code, 302)

    def test_view_does_not_raise_exception(self):
        request = self.factory.get(reverse('rides:match'), {'ride_id': self.ride.id, 'match_id': self.match.id, 'role': 'passenger'})
        request.user = self.user1
        try:
            match(request)
        except Exception as e:
            self.fail(f"The view raised an exception: {e}")


class DeclineViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user1 = User.objects.create_user(username='user1', password='testpassword1')
        self.user2 = User.objects.create_user(username='user2', password='testpassword2')
        ride = Ride.objects.create(user=self.user1, destination='D', origin='A', route=[[0.0, 0.0], [1.0, 1.0], [3.0, 3.0]], role='passenger',
                            origin_lat=0.0, origin_lon=0.0, destination_lat=3.0, destination_lon=3.0)
        ride.save()
        self.ride = ride
        match = Ride.objects.create(user=self.user2, destination='D', origin='A', route=[[0.0, 0.0], [1.0, 1.0], [3.0, 3.0]], role='driver',
                            origin_lat=0.0, origin_lon=0.0, destination_lat=3.0, destination_lon=3.0)
        match.save()
        self.match = match
        self.request = Request.objects.create(sender=self.match.user, receiver=self.ride.user, s_ride=self.match, r_ride=self.ride)

    def test_view_declines_ride(self):
        self.client.force_login(self.user1)
        request = self.factory.get(reverse('rides:decline'), {'ride_id': self.ride.id, 'match_id': self.match.id})
        request.user = self.user1
        req = Request.objects.create(sender=self.match.user, receiver=self.ride.user, s_ride=self.match, r_ride=self.ride)
        response = decline(request)
        self.assertEqual(response.status_code, 302)
        self.ride.refresh_from_db()
        self.match.refresh_from_db()
        self.request.refresh_from_db()
        self.assertEqual(self.request.status, Request.DECLINED)

    def test_invalid_ride_return_404(self):
    	self.client.force_login(self.user1)
    	request = self.factory.get(reverse('rides:decline'), {'ride_id': 999, 'match_id': self.match.id})
    	request.user = self.user1
    	response = decline(request)
    	self.assertEqual(response.status_code, 302)
        
    def test_view_requires_authentication(self):
        response = self.client.get(reverse('rides:decline'))
        self.assertEqual(response.status_code, 302)

    def test_view_does_not_raise_exception(self):
        request = self.factory.get(reverse('rides:decline'), {'ride_id': self.ride.id, 'match_id': self.match.id})
        request.user = self.user1
        try:
            decline(request)
        except Exception as e:
            self.fail(f"The view raised an exception: {e}")


class RequestViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user1 = User.objects.create_user(username='user1', password='testpassword1')
        self.user2 = User.objects.create_user(username='user2', password='testpassword2')
        ride = Ride.objects.create(user=self.user1, destination='D', origin='A', route=[[0.0, 0.0], [1.0, 1.0], [3.0, 3.0]], role='passenger',
                            origin_lat=0.0, origin_lon=0.0, destination_lat=3.0, destination_lon=3.0)
        ride.save()
        self.ride = ride
        match = Ride.objects.create(user=self.user2, destination='D', origin='A', route=[[0.0, 0.0], [1.0, 1.0], [3.0, 3.0]], role='driver',
                            origin_lat=0.0, origin_lon=0.0, destination_lat=3.0, destination_lon=3.0)
        match.save()
        self.match = match

    def test_view_requests_ride(self):
        self.client.force_login(self.user1)
        req = self.factory.get(reverse('rides:request'), {'ride_id': self.ride.id, 'match_id': self.match.id})
        req.user = self.user1
        response = request(req)
        req = Request.objects.filter(sender=self.user1, receiver=self.user2, s_ride=self.ride).first()
        self.assertEqual(response.status_code, 302)
        self.assertNotEqual(req, None)

    def test_invalid_ride_return_404(self):
    	self.client.force_login(self.user1)
    	req = self.factory.get(reverse('rides:request'), {'ride_id': 999, 'match_id': self.match.id})
    	req.user = self.user1
    	response = request(req)
    	self.assertEqual(response.status_code, 302)
        
    def test_view_requires_authentication(self):
        response = self.client.get(reverse('rides:request'))
        self.assertEqual(response.status_code, 302)

    def test_view_does_not_raise_exception(self):
        req = self.factory.get(reverse('rides:request'), {'ride_id': self.ride.id, 'match_id': self.match.id})
        req.user = self.user1
        try:
            request(req)
        except Exception as e:
            self.fail(f"The view raised an exception: {e}")
   

class EndTripViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.end_trip_url = reverse('rides:end_ride')

    def test_get_view_ends_ride(self):
        self.client.force_login(self.user)
        ride = Ride.objects.create(user=self.user, destination='D', origin='A', route=[[0.0, 0.0], [1.0, 1.0], [3.0, 3.0]], role='passenger',
                            origin_lat=0.0, origin_lon=0.0, destination_lat=3.0, destination_lon=3.0)
        req = self.factory.get(reverse('rides:end_ride'), {'ride_id': ride.id})
        req.user = self.user
        response = end_trip(req)
        ride.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ride.status, Ride.INACTIVE)
        
    def test_post_view_ends_ride(self):
        self.client.force_login(self.user)
        ride = Ride.objects.create(user=self.user, destination='D', origin='A', route=[[0.0, 0.0], [1.0, 1.0], [3.0, 3.0]], role='driver',
                            origin_lat=0.0, origin_lon=0.0, destination_lat=3.0, destination_lon=3.0)
        response = self.client.post(self.end_trip_url, {
            'ride_id': ride.id,
        })
        ride.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ride.status, Ride.INACTIVE)
        
    def test_post_view_creates_rating(self):
        self.client.force_login(self.user)
        user2 = User.objects.create_user(username='testuser2', password='testpassword2')
        ride = Ride.objects.create(user=self.user, destination='D', origin='A', route=[[0.0, 0.0], [1.0, 1.0], [3.0, 3.0]], role='driver',
                            origin_lat=0.0, origin_lon=0.0, destination_lat=3.0, destination_lon=3.0)
        response = self.client.post(self.end_trip_url, {
            'ride_id': ride.id,
            'rating': 4,
            'driver': 'testuser2'
        })
        rating = Rating.objects.filter(user=user2, rater=self.user, rate=4, ride=ride).first()
        self.assertEqual(response.status_code, 302)
        self.assertNotEqual(rating, None)
        
    def test_post_view_creates_review(self):
        self.client.force_login(self.user)
        user2 = User.objects.create_user(username='testuser2', password='testpassword2')
        ride = Ride.objects.create(user=self.user, destination='D', origin='A', route=[[0.0, 0.0], [1.0, 1.0], [3.0, 3.0]], role='driver',
                            origin_lat=0.0, origin_lon=0.0, destination_lat=3.0, destination_lon=3.0)
        response = self.client.post(self.end_trip_url, {
            'ride_id': ride.id,
            'review': 'Nice ride!',
            'driver': 'testuser2'
        })
        review = Review.objects.filter(user=user2, reviewer=self.user, review='Nice ride!', ride=ride).first()
        self.assertEqual(response.status_code, 302)
        self.assertNotEqual(review, None)

    def test_invalid_ride_return_404(self):
    	self.client.force_login(self.user)
    	req = self.factory.get(reverse('rides:end_ride'), {'ride_id': 999})
    	req.user = self.user
    	response = request(req)
    	self.assertEqual(response.status_code, 302)
        
    def test_view_requires_authentication(self):
        response = self.client.get(reverse('rides:end_ride'))
        self.assertEqual(response.status_code, 302)

    def test_view_does_not_raise_exception(self):
        ride = Ride.objects.create(user=self.user, destination='D', origin='A', route=[[0.0, 0.0], [1.0, 1.0], [3.0, 3.0]], role='driver',
                           origin_lat=0.0, origin_lon=0.0, destination_lat=3.0, destination_lon=3.0)
        req = self.factory.get(reverse('rides:end_ride'), {'ride_id': ride.id})
        req.user = self.user
        try:
            request(req)
        except Exception as e:
            self.fail(f"The view raised an exception: {e}")


class Error404ViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_view_returns_200_status_code(self):
        response = self.client.get(reverse('rides:404'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('rides:404'))
        self.assertTemplateUsed(response, 'rides/404.html')

    def test_view_does_not_require_authentication(self):
        response = self.client.get(reverse('rides:404'))
        self.assertFalse(response.has_header('WWW-Authenticate'))

    def test_view_does_not_raise_exception(self):
        response = self.client.get(reverse('rides:404'))
        self.assertNotEqual(response.status_code, 500) 
