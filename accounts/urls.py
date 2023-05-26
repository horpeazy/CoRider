from django.urls import path, include
from accounts.views import login_view, signup_view, logout_view

app_name = 'account'

urlpatterns = [
	path('register/', signup_view, name='signup'),
	path('login/', login_view, name='login'),
	path('logout/', logout_view, name='logout'),
]
