from django import forms
from django.contrib.auth import get_user_model
from rides.models import Vehicle, ContactMessage

User = get_user_model()


class VehicleForm(forms.ModelForm):
		make = forms.CharField(required=False)
		model = forms.CharField(required=False)
		color = forms.CharField(required=False)
		plate_number = forms.CharField(required=False)
		
		class Meta:
			model = Vehicle	
			fields = ('make', 'model', 'color', 'plate_number',)
			
		def is_empty(self):
			if ( not self.data['make'] and 
				 not self.data['model'] and
				 not self.data['color'] and
				 not self.data['plate_number'] ):
				return True
			return False
			
		def is_valid(self):
			valid = super().is_valid()
			if self.cleaned_data['make'] == '':
				self.add_error('make', 'make field is required.')
				valid = False
			
			if self.cleaned_data['model'] == '':
				self.add_error('model', 'model field is required.')
				valid = False
			
			if self.cleaned_data['color'] == '':
				self.add_error('color', 'color field is required.')
				valid = False
			
			if self.cleaned_data['plate_number'] == '':
				self.add_error('plate_number', 'plate number field is required.')
				valid = False	
			return valid

class ContactMessageForm(forms.ModelForm):
		name = forms.CharField(required=True)
		email = forms.EmailField(required=True)
		subject = forms.CharField(required=False)
		message = forms.CharField(required=True)
		
		class Meta:
			model = ContactMessage	
			fields = ('name', 'email', 'subject', 'message',)
