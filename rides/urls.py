from django.urls import path
from .views import home, contact

app_name = 'rides'

urlpatterns = [
    # Other URLs you want to include
    path('', home, name='home'),
    path('contact/', contact, name='contact'),
]
