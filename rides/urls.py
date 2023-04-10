from django.urls import path

from .views import home, about, contact, team, services

app_name = 'rides'

urlpatterns = [
    # Other URLs you want to include
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('team/', team, name='team'),
    path('services/', services, name='services'),
]
