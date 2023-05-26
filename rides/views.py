from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.db.models import Q, Avg
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from api.utils import match_routes
from rides.models import ( Ride, Review, Vehicle, 
						   Rating, Request, ContactMessage )
from accounts.forms import EditAccountForm
from rides.forms import VehicleForm, ContactMessageForm
import uuid
import ast
import json


User = get_user_model()

def home(request):
    context = {
    	'title': 'Home',
    	'cache_id': uuid.uuid4()
    }
    return render(request, 'rides/home.html', context)

def about(request):
    context = {
    	'title': 'About',
    	'cache_id': uuid.uuid4()
    }
    return render(request, 'rides/about.html', context)

def contact(request):
	context = {
    	'title': 'Contact',
    	'cache_id': uuid.uuid4(),
    	'form': ContactMessageForm()
    }
	if request.method == 'POST':
		contact_message_form = ContactMessageForm(request.POST)
		print(vars(contact_message_form))
		if contact_message_form.is_valid():
			contact_message_form.save()
			print("created")
			return redirect('rides:home')
		print("Error occured")
	return render(request, 'rides/contact.html', context)

def team(request):
    context = {
    	'title': 'Team',
    	'cache_id': uuid.uuid4()
    }
    return render(request, 'rides/team.html', context)

def services(request):
    context = {
    	'title': 'Services',
    	'cache_id': uuid.uuid4()
    }
    return render(request, 'rides/services.html', context)
    
def terms(request):
    context = {
    	'title': 'Terms',
    	'cache_id': uuid.uuid4()
    }
    return render(request, 'rides/terms.html', context)

def privacy(request):
    context = {
    	'title': 'Privacy',
    	'cache_id': uuid.uuid4()
    }
    return render(request, 'rides/privacy.html', context)

@login_required   
def ride(request):
    context = {
    	'title': 'Ride',
    	'cache_id': uuid.uuid4()
    }
    return render(request, 'rides/ride.html',  context)

@login_required   
def rides(request):
	rides = Ride.objects.filter(user=request.user).all()
	context = {
		'title': 'Rides',
		'rides': rides[::-1],
		'cache_id': uuid.uuid4()
	}
	return render(request, 'rides/rides.html',  context)
	
@login_required   
def reviews(request):
	reviews = Review.objects.filter(user=request.user).all()
	context = {
		'title': 'Reviews',
		'reviews': reviews,
		'cache_id': uuid.uuid4()
	}
	return render(request, 'rides/reviews.html',  context)
	
@login_required   
def profile_reviews(request, username):
	user = User.objects.filter(username=username).first()
	reviews = Review.objects.filter(user=user).all()
	context = {
		'title': 'Profile Reviews',
		'reviews': reviews,
		'cache_id': uuid.uuid4()
	}
	return render(request, 'rides/reviews.html',  context)

@login_required    
def account(request):
	user = request.user
	vehicle = Vehicle.objects.filter(user=user).first()
	user_ratings = Rating.objects.filter(user=user)
	total_requests = Request.objects.filter(receiver=user).all()
	accepted_requests = Request.objects.filter(receiver=user, 
										status=Request.ACCEPTED).all()
	if len(total_requests) > 0:
		availability = ( len(accepted_requests) * 100 ) / len(total_requests)
		user.availability = int(availability)
	context = {
		'title': 'Account Information',
		'user': user,
		'vehicle': vehicle,
		'cache_id': uuid.uuid4()
	}
	return render(request, 'rides/account.html', context)
    
@login_required    
def edit_account(request):
	account = request.user
	vehicle = Vehicle.objects.filter(user=request.user).first()
	if request.method == "POST":
		account_form = EditAccountForm(request.POST, request.FILES, instance=account)
		if vehicle:
			vehicle_form = VehicleForm(request.POST, instance=vehicle)
		else:
			vehicle_form = VehicleForm(request.POST)
		if vehicle_form.is_empty():
			if account_form.is_valid():
				account = account_form.save(commit=False)
				account.verified = True
				account.save()
				if vehicle:
					vehicle.delete()
				return redirect('rides:account')
		else:
			if account_form.is_valid() and vehicle_form.is_valid():
				account = account_form.save(commit=False)
				vehicle = vehicle_form.save(commit=False)
				account.verified = True
				vehicle.user = request.user
				account.save()
				vehicle.save()
				return redirect('rides:account')
	else:
		account_form = EditAccountForm(instance=account)
		if vehicle:
			vehicle_form = VehicleForm(instance=vehicle)
		else:
			vehicle_form = VehicleForm()
	context = {
		'title': 'Edit Account',
		'account_form': account_form,
		'vehicle_form': vehicle_form,
		'cache_id': uuid.uuid4()
	}
	return render(request, 'rides/edit-account.html', context)

@login_required
def profile(request, username):
	user = User.objects.get(username=username)
	vehicle = Vehicle.objects.filter(user=user).first()
	user_ratings = Rating.objects.filter(user=user)
	total_requests = Request.objects.filter(receiver=user).all()
	accepted_requests = Request.objects.filter(receiver=user,
										status=Request.ACCEPTED).all()
	if len(total_requests) > 0:
		availability = ( len(accepted_requests) * 100 ) / len(total_requests)
		user.availability = int(availability)
	context = {
		'title': 'Profile',
    	'user': user,
    	'vehicle': vehicle,
    	'cache_id': uuid.uuid4()
    }
	return render(request, 'rides/profile.html', context)   

@login_required
def ride_detail(request, ride_id):
	ride = Ride.objects.filter(user=request.user, id=ride_id).first()
	if not ride:
		return JsonResponse({ "message": "not found"}, status=404)
	matches = []    # possible matches
	requests = Request.objects.filter(receiver=request.user, r_ride=ride, 
									  status=Request.PENDING).all()
	sent_requests_q = Request.objects.filter(sender=request.user, s_ride=ride,
										   status=Request.PENDING).all()
	request_rides = []
	sent_requests = []
	for r in requests:
		request_rides.append(r.s_ride)
	for r in sent_requests_q:
		sent_requests.append(r.r_ride)
	if ride.role == "passenger":	
		if ride.status == Ride.ACTIVE or ride.status == Ride.PENDING:
			rides = Ride.objects.filter(role=Ride.DRIVER).\
				     exclude(Q(user=request.user)).\
				     exclude(Q(status=Ride.INACTIVE))
			for mride in rides:
				# Convert the route string to a list of coordinates.
				ride_route = ast.literal_eval(mride.route)
				match_rate = match_routes(ast.literal_eval(ride.route), ride_route)
				# add the match to potential matches if it's not the driver
				if ( match_rate >= 0.4 and mride.user != ride.driver 
				     and mride not in request_rides and mride not in sent_requests):
					mride.match_rate = match_rate * 100
					mride.username = mride.user.username
					mride.profile_picture = mride.user.profile_picture.url
					mride.rating = mride.user.rating
					matches.append(vars(mride))
	else:	
		if ride.status == Ride.ACTIVE or ride.status == Ride.PENDING:
			rides = Ride.objects.filter(role=Ride.PASSENGER, status=Ride.PENDING).\
						    exclude(Q(user=request.user))
			for mride in rides:
				# Convert the route string to a list of coordinates.
				ride_route = ast.literal_eval(mride.route)
				match_rate = match_routes(ast.literal_eval(ride.route), ride_route)
				if ( match_rate >= 0.4 and mride not in ride.passengers.all()
				     and mride not in request_rides and mride not in sent_requests ):
					mride.match_rate = match_rate * 100
					mride.username = mride.user.username
					mride.profile_picture = mride.user.profile_picture.url
					mride.rating = mride.user.rating
					matches.append(vars(mride))
	passengers = ride.passengers.all()
	driver = ride.driver
	ride.user_id = ride.user.id
	ride = vars(ride)
	ride["requests"] = request_rides
	ride["passengers"] = passengers
	ride["driver"] = driver
	context = {
		"title": "Ride Detail",
		"ride": ride,
		"matches": matches,
		"cache_id": uuid.uuid4(),
	}
	return render(request, "rides/ride-detail.html", context)

@login_required
def match(request):
	ride_id = request.GET.get("ride_id", None)
	match_id = request.GET.get("match_id", None)
	role = request.GET.get("role", None)
	ride = Ride.objects.filter(id=ride_id).first()
	match = Ride.objects.filter(id=match_id).first()
	req = Request.objects.\
				  filter(sender=match.user, receiver=ride.user,s_ride=match).\
				  first()
	if ride and match:
		if role == "passenger":
			ride.driver = match
			match.passengers.add(ride)
		else:
			ride.passengers.add(match)
			match.driver = ride
		req.status = Request.ACCEPTED
		ride.save()
		match.save()
		req.save()
		return redirect("rides:ride-detail", ride_id=ride_id)  
	else:
		return render(request, "rides/404.html", context)
	
@login_required	
def decline(request):
	ride_id = request.GET.get("ride_id")
	match_id = request.GET.get("match_id")
	ride = Ride.objects.filter(id=ride_id).first()
	match = Ride.objects.filter(id=match_id).first()
	if ride and match:
		req = Request.objects.\
					  filter(sender=match.user,receiver=ride.user,r_ride=ride).\
					  first()
		req.status = Request.DECLINED
		req.save()
		return redirect("rides:ride-detail", ride_id=ride_id)
	else:
		return render(request, "rides/404.html", context)

@login_required    
def request(request):
	ride_id = request.GET.get('ride_id', None)
	match_id = request.GET.get('match_id', None)
	ride = Ride.objects.filter(id=ride_id).first()
	match = Ride.objects.filter(id=match_id).first()

	if ride and match:
		Request.objects.create(sender=ride.user, receiver=match.user,
							   r_ride=match, s_ride=ride)
	return redirect("rides:ride-detail", ride_id=ride_id)

@login_required	
def end_trip(request):
	if request.method == "POST":
		ride_id = request.POST.get("ride_id")
		driver_name = request.POST.get("driver")
		review = request.POST.get("review")
		rate = request.POST.get("rating", 0)
		ride = Ride.objects.filter(user=request.user, id=ride_id).first()
		user = User.objects.get(username=driver_name)
		if rate:
				rating = Rating.objects.create(user=user, rate=rate,
											   rater=request.user, ride=ride)
				user_ratings = Rating.objects.filter(user=user)
				if user_ratings:
					average_rating = user_ratings.aggregate(Avg('rate'))['rate__avg']
					user.rating = round(average_rating, 1)
					user.save()
		if review:
			review = Review.objects.create(user=user, review=review, rating=rate,
						       reviewer=request.user, ride=ride)
	else:
		ride_id = request.GET.get("ride_id")
		ride = Ride.objects.filter(user=request.user, id=ride_id).first()
	if ride:
		ride.status = Ride.INACTIVE
		user = User.objects.filter(username=request.user.username).first()
		user.total_rides += 1
		if ride.role == 'driver':
			user.as_driver += 1
		else:
			user.as_passenger += 1
		user.save()
		ride.save()
	return redirect("rides:ride-detail", ride_id)

@login_required
@csrf_exempt
def create_review(request):
	if request.method == "POST":
		request_body = json.loads(request.body)
		review = request_body.get("review")
		user_id = request_body.get("user_id")
		ride_id = request_body.get("ride_id")
		rating = request_body.get("rating")
		ride = Ride.objects.filter(id=ride_id).first()
		user = User.objects.filter(id=user_id).first()
		if rating == '':
			rating = 0
		if rating:
			Rating.objects.create(user=user, rate=rating,
								  rater=request.user, ride=ride)
			user_ratings = Rating.objects.filter(user=user)
			if user_ratings:
				average_rating = user_ratings.aggregate(Avg('rate'))['rate__avg']
				user.rating = round(average_rating, 1)
				user.save()
		if review:
			Review.objects.create(user=user, review=review, rating=rating,
						          reviewer=request.user, ride=ride)
		response = {
			"message": 'Created Successfully'
		}
		return JsonResponse(response, status=201)
		


