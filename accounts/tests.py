from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.forms import SignUpForm

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
        self.assertFormError(response, 'form', 'password2', 'This password is too short. It must contain at least 8 characters.')

