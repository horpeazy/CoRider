from django.urls import path
from .views import ( find_match, create_review, 
					 email_subscription )

app_name = 'api'

urlpatterns = [
    # Other URLs you want to include
    path('match/', find_match, name='find_match'),
    path('review/create/', create_review, name='create_review'),
    path('subscription/create/', email_subscription, name='email_subscription'),
]
