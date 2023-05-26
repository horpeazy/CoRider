from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q, Avg
from rides.models import Ride, Vehicle, Rating, Review
from accounts.forms import EditAccountForm
from rides.forms import VehicleForm
from .utils import match_routes
import json
import ast
import datetime

# Create your views here.

User = get_user_model()


@login_required
@csrf_exempt
def find_match(request):
	if request.method == 'POST':
		if not request.user.verified:
			response = {
				'status': 401
				'message': 'Unauthorized'
			}
			return JsonResponse(response, status=401)
		request_body = json.loads(request.body)
		route = request_body.get('route')
		role = request_body.get('role')
		destination = request_body.get('destination')
		origin = request_body.get('location')
		origin_lat = request_body.get('origin_lat')
		origin_lon = request_body.get('origin_lon')
		destination_lat = request_body.get('destination_lat')
		destination_lon = request_body.get('destination_lon')
		# Cancel former rides and save the new trip
		rides = Ride.objects.filter(user=request.user).exclude(Q(status=Ride.INACTIVE))
		user = User.objects.filter(username=request.user.username).first()
		for ride in rides:
			ride.status = Ride.INACTIVE
			user.total_rides += 1
			if ride.role == 'driver':
				user.as_driver += 1
			else:
				user.as_passenger += 1
			user.save()
			ride.save()
		new_ride = Ride.objects.create(user=request.user, destination=destination, origin=origin,
					       route=route, role=role,
					       origin_lat=origin_lat, origin_lon=origin_lon,
					       destination_lat=destination_lat, 
					       destination_lon=destination_lon)
		# set the trip as the drivers or passenger trip
		if role == 'driver':
			new_ride.driver = new_ride
		new_ride.save()

		# find matches in the db
		if role == 'driver':
			trips = Ride.objects.filter(role=Ride.PASSENGER, status=Ride.PENDING)
		else:
			trips = Ride.objects.filter(role=Ride.DRIVER, status=Ride.PENDING)
		matches = []
		for trip in trips:
			trip_route = ast.literal_eval(trip.route)
			match_rate = match_routes(route, trip_route)
			if  match_rate >= 0.4:
				matches.append({
					'id': trip.id,
					'ride_id': new_ride.id,
					'username': trip.user.username,
					'user_rating': trip.user.rating,
					'profile_picture': trip.user.profile_picture.url,
					'destination': trip.destination,
					'origin': trip.origin,
					'match_rate': match_rate * 100,
					'role': trip.role
				})
		return JsonResponse({'result': matches, 'id': new_ride.id}, status=200)
	else:
		response = {
			'message': 'Method not allowed'
		}
		return JsonResponse(response, status=403)

@login_required
@csrf_exempt
def create_review(request):
	if request.method == 'POST':
		request_body = json.loads(request.body)
		review = request_body.get('review')
		user_id = request_body.get('user_id')
		ride_id = request_body.get('ride_id')
		rating = request_body.get('rating')
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
			'status': 201
			'message': 'Created Successfully'
		}
		return JsonResponse(response, status=201)
