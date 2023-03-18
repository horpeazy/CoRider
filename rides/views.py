from django.shortcuts import render
import uuid

# Create your views here.


def home(request):
    context = {
    	'title': 'Corider',
    	'cache_id': uuid.uuid4()
    }
    return render(request, 'rides/home.html', { 'context': context })
