from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from accounts.views import login_view, logout_view
from django.contrib.auth import get_user_model
from accounts.forms import SignUpForm, LoginForm
from django.contrib.auth.forms import AuthenticationForm

User = get_user_model()

class SignUpViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('accounts:signup')
    
    def test_get_request(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signup.html')
        self.assertIsInstance(response.context['form'], SignUpForm)
    
    def test_post_request_with_valid_data(self):
        response = self.client.post(self.signup_url, {
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
        })
        self.assertRedirects(response, reverse('rides:home'))
        self.assertTrue(User.objects.filter(username='testuser').exists())
        self.assertTrue(response.wsgi_request.user.is_authenticated)
    
    def test_post_request_with_invalid_data(self):
        response = self.client.post(self.signup_url, {
            'username': '',
            'password1': 'password',
            'password2': 'different_password',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signup.html')
        self.assertFormError(response, 'form', 'username', 'This field is required.')
        self.assertFormError(response, 'form', 'password2', 'The two password fields didn’t match.')
    
    def test_form_validation_required_fields(self):
        form = SignUpForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('password1', form.errors)
        self.assertIn('password2', form.errors)

    def test_post_request_existing_user(self):
        User.objects.create_user(username='existinguser', password='password')
        response = self.client.post(self.signup_url, {
            'username': 'existinguser',
            'password1': 'testpassword',
            'password2': 'testpassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertFormError(response, 'form', 'username', 'User with this Username already exists.')
    
    def test_post_request_different_passwords(self):
        response = self.client.post(self.signup_url, {
            'username': 'testuser',
            'password1': 'password1',
            'password2': 'password2',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertFormError(response, 'form', 'password2', 'The two password fields didn’t match.')
    
    def test_post_request_missing_required_fields(self):
        response = self.client.post(self.signup_url, {})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertFormError(response, 'form', 'username', 'This field is required.')
        self.assertFormError(response, 'form', 'password1', 'This field is required.')
        self.assertFormError(response, 'form', 'password2', 'This field is required.')
    
    def test_post_request_valid_data_redirect(self):
        response = self.client.post(self.signup_url, {
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
        })
        self.assertRedirects(response, reverse('rides:home'))
        self.assertTrue(User.objects.filter(username='testuser').exists())
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        
    def test_post_request_long_username(self):
    	response = self.client.post(self.signup_url, {
        	'username': 'a' * 256,  # Long username with 256 characters
        	'password1': 'testpassword',
        	'password2': 'testpassword',
        })
    	self.assertEqual(response.status_code, 200)
    	self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_post_request_short_password(self):
    	response = self.client.post(self.signup_url, {
        	'username': 'newUser',
        	'password1': 'abc',
        	'password2': 'abc',
    	})
    	self.assertEqual(response.status_code, 200)
    	self.assertFalse(response.wsgi_request.user.is_authenticated)

    	password2_errors = response.context['form'].errors.get('password2', [])
    	expected_errors = [
        	'This password is too short. It must contain at least 8 characters.',
        	'This password is too common.'
    	]

    	self.assertTrue(any(error in password2_errors for error in expected_errors))


class LoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('accounts:login')
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_get_request(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
        self.assertIsInstance(response.context['form'], AuthenticationForm)

    def test_valid_credentials(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpassword',
        })
        self.assertRedirects(response, '/')
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_invalid_credentials(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
        self.assertFormError(response, 'form', None, 'Please enter a correct username and password. Note that both fields may be case-sensitive.')

    def test_missing_username(self):
        response = self.client.post(self.login_url, {
            'password': 'testpassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
        self.assertFormError(response, 'form', 'username', 'This field is required.')

    def test_missing_password(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
        self.assertFormError(response, 'form', 'password', 'This field is required.')

    def test_empty_fields(self):
        response = self.client.post(self.login_url, {
            'username': '',
            'password': '',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
        self.assertFormError(response, 'form', 'username', 'This field is required.')
        self.assertFormError(response, 'form', 'password', 'This field is required.')

    def test_authenticated_user(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.login_url)
        self.assertRedirects(response, '/')
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_next_parameter(self):
        response = self.client.post(self.login_url + '?next=/account', {
            'username': 'testuser',
            'password': 'testpassword',
        })
        self.assertEqual(response.status_code, 302)

    def test_invalid_next_parameter(self):
        response = self.client.post(self.login_url + '?next=http://malicious.com', {
            'username': 'testuser',
            'password': 'testpassword',
        })
        self.assertEqual(response.status_code, 302)


class LogoutViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.logout_url = reverse('accounts:logout')
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_logout_authenticated_user(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.logout_url)
        self.assertRedirects(response, '/')
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_logout_unauthenticated_user(self):
        response = self.client.get(self.logout_url)
        self.assertRedirects(response, '/')
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_logout_redirect_home(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.logout_url)
        self.assertRedirects(response, '/')

    def test_logout_post_request(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.logout_url)
        self.assertRedirects(response, '/')
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_logout_no_user(self):
        response = self.client.get(self.logout_url)
        self.assertRedirects(response, '/')
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_logout_with_other_data(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.logout_url, data={'key': 'value'})
        self.assertRedirects(response, '/')
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_logout_with_invalid_user(self):
        self.client.login(username='testuser', password='testpassword')
        self.user.delete()
        response = self.client.get(self.logout_url)
        self.assertRedirects(response, '/')
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_logout_with_extra_path(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.logout_url + 'extra/path')
        self.assertEqual(response.status_code, 404)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_logout_with_query_parameter(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.logout_url + '?next=/accounts/profile')
        self.assertRedirects(response, '/')
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_logout_with_invalid_method(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 302)

