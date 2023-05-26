from django.urls import path

from .views import ( home, about, contact, 
		             team, services, ride,
		     		 match, ride_detail,
		     		 end_trip, request, decline, 
		     		 account, profile, 
		     		 edit_account, rides,
		     		 reviews, terms, privacy,
		     		 profile_reviews )

app_name = 'rides'

urlpatterns = [
    # Other URLs you want to include
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('team/', team, name='team'),
    path('services/', services, name='services'),
    path('ride/', ride, name='ride'),
    path('rides/', rides, name='rides'),
    path('ride-detail/<int:ride_id>', ride_detail, name='ride-detail'),
    path('request/', request, name='request'),
    path("end-ride/", end_trip, name="end_trip"),
    path("match/", match, name="match"),
    path("decline/", decline, name="decline"),
    path("account/", account, name="account"),
    path("account/edit", edit_account, name="edit_account"),
    path("profile/<str:username>", profile, name="profile"),
    path("reviews/", reviews, name="reviews"),
    path("reviews/<str:username>", profile_reviews, name="profile_reviews"),
    path("terms/", terms, name="terms"),
    path("privacy/", privacy, name="privacy"),
]
