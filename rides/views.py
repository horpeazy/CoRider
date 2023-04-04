from django.shortcuts import render
import uuid

# Create your views here.


def home(request):
    context = {
    	'title': 'Home',
    	'cache_id': uuid.uuid4()
    }
    return render(request, 'rides/home.html', { 'context': context })


def about(request):
    context = {
    	'title': 'About',
    	'cache_id': uuid.uuid4()
    }
    return render(request, 'rides/about.html', { 'context': context })

def contact(request):
    context = {
    	'title': 'Contact',
    	'cache_id': uuid.uuid4()
    }
    return render(request, 'rides/contact.html', { 'context': context })

def team(request):
    context = {
    	'title': 'Team',
    	'cache_id': uuid.uuid4()
    }
    return render(request, 'rides/team.html', { 'context': context })