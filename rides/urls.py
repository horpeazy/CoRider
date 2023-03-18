from django.urls import path
from .views import home

app_name = 'rides'

urlpatterns = [
    # Other URLs you want to include
    path('', home, name='home'),
]
