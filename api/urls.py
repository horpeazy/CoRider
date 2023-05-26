from django.urls import path
from .views import find_match

app_name = 'api'

urlpatterns = [
    # Other URLs you want to include
    path('match/', find_match, name='find_match'),
]
