from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class SignUpForm(UserCreationForm):
	username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True}), 
							   required=True)
	

	class Meta:
		model = User
		fields = ('username', 'password1', 'password2')


class LoginForm(AuthenticationForm):
	username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True}), 
							   required=True)
	
	class Meta:
		model = User
		fields = ('username', 'password')


class EditAccountForm(forms.ModelForm):
	first_name = forms.CharField(required=True)
	last_name = forms.CharField(required=True)
	gender = forms.ChoiceField(required=True, choices=User.GENDER_CHOICES)
	phone_number = forms.CharField(required=True)
	address = forms.CharField(required=True)
	class Meta:
		model = User
		fields = ('first_name', 'last_name',
				  'gender', 'birthday',
				  'email' , 'phone_number', 
				  'address', 'zip_code',
				  'driver_id', 'profile_picture', )
		widgets = {
			'birthday': forms.DateInput(attrs={'type': 'date'})
		}

