let marker, circle, dMarker, zoomed;
let currenRroute, currentDest, current_location;
const west = 30.8203
const south = 38.6769
const east = 33.8558
const north = 40.7537
const center = [8.6753, 9.0820];

mapboxgl.accessToken = 'pk.eyJ1IjoiaG9ycGVhenkiLCJhIjoiY2xmNjFuOGJyMWk0bzN2cjBzZno0NXNmdCJ9.aEgc6K_vrA2mctaeIFzBrg';

// Create a new Mapbox map
const map = new mapboxgl.Map({
	container: 'map',
	projection: 'globe',
	style: 'mapbox://styles/horpeazy/clf7ms36k001c01qoerxs6zdt',
	center: center,
	zoom: 13,
	zoomControl: true
});

// Add a marker to the map
marker = new mapboxgl.Marker()
	.setLngLat([startLon, startLat])
	.addTo(map);
	
map.addControl(new mapboxgl.NavigationControl(), 'top-left');


// Declare function to draw map
function drawRoute(startLat, startLon, endLat, endLon) {
	const routeUrl = "https://api.mapbox.com/directions/v5/mapbox/driving";
	const options = "geometries=geojson&overview=full";
	fetch(`${routeUrl}/${startLon},${startLat};${endLon},${endLat}?${options}&access_token=${mapboxgl.accessToken}`)
	.then(function (response) {
			if (!response.ok) {
				throw new Error(`HTTP error! status: ${response.status}`);
			}
			return response.json();
	})
	.then(function (json) {
			// Check if the response contains a valid route object
			if (!json.routes || json.routes.length === 0) {
				throw new Error('No route found.');
			}

			// Get the first route from the response
			const route = json.routes[0];

			// Create a GeoJSON object from the route geometry
			const routeGeoJSON = {
				type: 'Feature',
				properties: {},
				geometry: route.geometry,
			};

			// Add the route layer to the map
			map.addLayer({
				id: 'route',
				type: 'line',
				source: {
					type: 'geojson',
					data: routeGeoJSON,
				},
				layout: {
					'line-join': 'round',
					'line-cap': 'round',
				},
				paint: {
					'line-color': 'red',
					'line-width': 4,
				},
			});

			dMarker = new mapboxgl.Marker()
				.setLngLat([endLon, endLat])
				.addTo(map);

			// Fit the map view to the route bounds
			const bounds = new mapboxgl.LngLatBounds();
			routeGeoJSON.geometry.coordinates.forEach((coord) => bounds.extend(coord));
			map.fitBounds(bounds, { padding: 50 });
		})
		.catch(error => {
			console.log(error);
		})
}

drawRoute(startLat, startLon, endLat, endLon);

if (trip.status === 'active') {
	navigator.geolocation.watchPosition(success, error);

	function success(pos) {
		currentLocationtLat = pos.coords.latitude;
		currentLocationLon = pos.coords.longitude;
		if (currentLocationMarker) {
			currentLocationMarker.remove();
		}
		currentLocationMarker = new mapboxgl.Marker({
												icon: {
    												url: "https://api.mapbox.com/styles/v1/mapbox/streets-v11/icons/marker-15.svg",
    												size: 25,
    												color: "red"
  												}
											})
											.setLngLat([currentLocationLon, currentLocationtLat])
											.addTo(map);
		map.setCenter([currentLocationLon, currentLocationtLat]);
	}
	
	function error(err) {
			if (err.code === 1) {
				alert("Please allow geolocation access");
			} else {
				alert("Cannot get current location");
		}
	}
}

