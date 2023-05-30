from django.shortcuts import render, redirect
from django.contrib.auth import ( logout, authenticate,
								 login, get_user_model )
from accounts.forms import SignUpForm
from django.contrib.auth.forms import AuthenticationForm
import uuid

# Create your views here.

User = get_user_model()


def signup_view(request):
	if request.method == 'GET':
		form = SignUpForm()
	else:
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			return redirect('rides:home')
	context = {
		'title': 'Sign Up',
		'cache_id': uuid.uuid4(),
		'form': form
	}
	return render(request, 'accounts/signup.html', context)

	
def login_view(request):
	if request.user.is_authenticated:
		return redirect('rides:home')
	if request.method == 'GET':
		form = AuthenticationForm()
	else:
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get("username")
			password = form.cleaned_data.get("password")
			user = authenticate(request, username=username, password=password)
			if user is not None:
				next = request.GET.get('next', '/')
				login(request, user)
				return redirect(next)
			else:
				form.add_error(None, "Invalid username or password")
	context = {
		'title': 'Login',
		'cache_id': uuid.uuid4(),
		'form': form
	}
	return render(request, 'accounts/login.html', context)
	
def logout_view(request):
	if request.user:
		logout(request)
		return redirect('rides:home')
	return redirect('rides:home')

