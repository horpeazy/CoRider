const searchInput = document.querySelector(".destination");
const locations = document.querySelector(".locations");
const locationItems = document.querySelectorAll(".location");
const searchEl = document.querySelector('.search');
const resultsEl = document.querySelector('.results-wrapper');
const matchesEl = document.querySelector('.match-result');
const personEl = document.querySelector('.fa-person');
const carEl = document.querySelector('.fa-car');
const matchBtn = document.querySelector('.fa-search');
let zoomed, dMarker, endLon, endLat, startLat, startLon;
let currenRoute, currentDest, current_location;
let role;
const west = 30.8203;
const south = 38.6769;
const east = 33.8558;
const north = 40.7537;
const center = [39.9334, 32.8597];

mapboxgl.accessToken = 'pk.eyJ1IjoiaG9ycGVhenkiLCJhIjoiY2xmNjFuOGJyMWk0bzN2cjBzZno0NXNmdCJ9.aEgc6K_vrA2mctaeIFzBrg';

// Create a new Mapbox map
const map = new mapboxgl.Map({
    container: 'map',
    projection: 'globe',
    style: 'mapbox://styles/horpeazy/clf7ms36k001c01qoerxs6zdt',
    center: [32.8597, 39.9334],
    zoom: 15,
});

// Add a marker to the map
let marker = new mapboxgl.Marker()
    .setLngLat([32.8597, 39.9334])
    .addTo(map);

// When the marker is clicked, show the Street View panorama
marker.getElement().addEventListener('click', function() {
    const panorama = new mapboxgl.Popup({
        closeButton: true,
        closeOnClick: false,
        anchor: 'top-left',
        offset: [0, 0]
    });

    panorama.setDOMContent(document.getElementById('panorama'));

    const panoramaOptions = {
        position: {
            lat: startLat, 
            lng: startLon
        },
        pov: {
            heading: 0,
            pitch: 0
        }
    };

    // Create a new Street View panorama
    const streetView = new mapboxgl.StreetViewPanorama(panoramaOptions);

    // Add the Street View panorama to the map
    map.addControl(streetView);

    // Open the Street View panorama in the popup
    panorama.setLngLat(marker.getLngLat()).addTo(map);
});
    
map.addControl(new mapboxgl.NavigationControl(), 'top-left');
    
    
    // Direction Form
const directions = new MapboxDirections({
        accessToken: mapboxgl.accessToken
    })

function direction_reset() {
        directions.actions.clearOrigin()
        directions.actions.clearDestination()
        directions.container.querySelector('input').value = ''
}
$(function() {
        $('#get-direction').click(function() {
            // Adding Direction form and instructions on map
            map.addControl(directions, 'top-left');
            directions.container.setAttribute('id', 'direction-container')
            $(geocoder.container).hide()
            $(this).hide()
            $('#end-direction').removeClass('d-none')
            $('.marker').remove()
        })
        $('#end-direction').click(function() {
            direction_reset()
            $(this).addClass('d-none')
            $('#get-direction').show()
            $(geocoder.container).show()
            map.removeControl(directions)
        })
})

function drawRoute(startLat, startLon, endLat, endLon) {
    let routeUrl = "https://api.mapbox.com/directions/v5/mapbox/driving";
    const options = "geometries=geojson&overview=full";
    fetch(`${routeUrl}/${startLon},${startLat};${endLon},${endLat}?${options}&access_token=${mapboxgl.accessToken}`)
    .then(function (response) {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response}`);
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
            const lineString = route.geometry;
                currentRoute = [];
                for (var i = 0; i < lineString.coordinates.length; i++) {
                    currentRoute.push([lineString.coordinates[i][1], lineString.coordinates[i][0]]);
                }

            // Create a GeoJSON object from the route geometry
            const routeGeoJSON = {
                type: 'Feature',
                properties: {},
                geometry: route.geometry,
            };

            // Add the route layer to the map
            if (map.getLayer('route')) {
                map.removeLayer('route');
            }
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
                visibility: 'visible'
            });

            const dMarker = new mapboxgl.Marker()
                .setLngLat([endLon, endLat])
                .addTo(map);

            // Fit the map view to the route bounds
            const bounds = new mapboxgl.LngLatBounds();
            routeGeoJSON.geometry.coordinates.forEach((coord) => bounds.extend(coord));
            map.fitBounds(bounds, { padding: 50 });        
        });
}

function distance(lat1, lon1, lat2, lon2) {
    lat1 = parseFloat(lat1);
    lat2 = parseFloat(lat2);
    lon1 = parseFloat(lon1);
    lon2 = parseFloat(lon2);
    const R = 6371; // radius of the earth in km
    const dLat = (lat2 - lat1) * (Math.PI / 180);
    const dLon = (lon2 - lon1) * (Math.PI / 180);
    const a = Math.sin(dLat/2) * Math.sin(dLat/2) + Math.cos(lat1 * (Math.PI / 180)) * Math.cos(lat2 * (Math.PI / 180)) * Math.sin(dLon/2) * Math.sin(dLon/2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    const d = R * c;
    return d;
}


navigator.geolocation.watchPosition(success, error, { enabledHighAccuracy: true });

function success(pos) {
    startLat = pos.coords.latitude;
    startLon = pos.coords.longitude;
    const placesUrl = "https://api.mapbox.com/geocoding/v5/mapbox.places";
    const geocodeUrl = `${placesUrl}/${startLon},${startLat}.json?access_token=${mapboxgl.accessToken}`;
    fetch(geocodeUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error("Network error: could not fetch current location");
            }
            return response.json();
        })
        .then(data => {
            current_location = data.features[0].place_name;
            // Remove existing marker and circle
            if (marker) {
                marker.remove();
            }
            if (dMarker) {
                dMarker.remove();
            }
            marker = new mapboxgl.Marker().setLngLat([startLon, startLat]).addTo(map);
            
            if (endLon && endLat) {
                drawRoute(startLat, startLon, endLat, endLon);
            } else {
                map.setCenter([startLon, startLat]);
            }
        })
        .catch(error => {
            console.error("Error:", error);
        });
}


function error(err) {
        if (err.code === 1) {
            alert("Please allow geolocation access");
        } else {
            alert("Cannot get current location");
    }
}


searchInput.addEventListener("focus", ()=> {
    locations.style.display = "block";
})

searchInput.addEventListener("blur", (e)=> {
    if (e.relatedTarget && !e.relatedTarget.classList.contains("destination")) {
        locations.style.display = "none";
    }	
})

resultsEl.addEventListener("blur", (e)=> {
    if (e.relatedTarget && !e.relatedTarget.classList.contains("results")) {
        resultsEl.style.top = "100vh";
    }	
})

searchInput.addEventListener("keyup", ()=> {
    const value = searchInput.value;
    if (value.length > 2) {
        locations.innerHTML = "";
        fetch(`https://nominatim.openstreetmap.org/search?q=${value}&format=json`)
            .then(response => response.json())
            .then(data => {
                // Do something with the latitude and longitude
                let locationsContent = "";
                for (let i = 0; i < data.length; i++) {
                    d = distance(startLat, startLon, data[i].lat, data[i].lon);
                    locationsContent  +=   `<li class="location" data-lat=${data[i].lat} data-lon=${data[i].lon} data-dest='${data[i].display_name}'>
                                                <span class="l-span">
                                                    <i class="fas fa-map-marker-alt icon"></i>
                                                    <span class="dist">${d.toFixed(2)}km</span>
                                                </span>
                                                ${data[i].display_name}
                                            </li>`;
                }
                if (locationsContent !== "") {
                    locations.innerHTML = locationsContent;
                }
                const locationItems = document.querySelectorAll(".location");
                locationItems.forEach(item => {
                    item.addEventListener('click', (e) => {
                        searchEl.style.display = 'none';
                        searchEl.style.top = '100%'
                        endLon = e.target.getAttribute("data-lon");
                        endLat = e.target.getAttribute("data-lat");
                        currentDest = e.target.getAttribute("data-dest");
                        locations.style.display = "none";
                        searchInput.value = currentDest;
                        drawRoute(startLat, startLon, endLat, endLon);
                    });
                });
            })
            .catch(error => console.log(error));
    }
});

matchBtn.addEventListener("click", (e) => {
	    if ( !(endLat && endLon) ) {
	    	alert("Please enter a destination");
	    	return;
	    }
	    resultsEl.style.top = 'calc(21vh + 10px)';
	    const spinnerBox = document.createElement('div');
	    spinnerBox.classList.add('spinner-box');
	    spinnerBox.innerHTML = `<div class="spinner">
	    				<div id="spinner"></div>
	    				<p>Finding Match</p>
	    		            </div>
	    			   `; 
	    resultsEl.appendChild(spinnerBox);
            routeUrl = "https://router.project-osrm.org/route/v1/driving/";
            //url = routeUrl + startLon + ',' + startLat + ';' + endLon + ',' + endLat + '?geometries=geojson&overview=full'
            fetch("/api/v1/match/", {
                    method: "POST",
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        route: currentRoute,
                        destination: currentDest,
                        location: current_location,
                        origin_lat: startLat,
                        origin_lon: startLon,
                        destination_lat: endLat,
                        destination_lon: endLon,
                        role: role,
                    })
                })
            .then(function (response) {
                return response.json();
            })
            .then(function (json) {
                // Parse the response and create a LatLng array for the route
                //const route = json.routes[0];
                //const lineString = route.geometry;
                //currentRoute = [];
                //for (var i = 0; i < lineString.coordinates.length; i++) {
                //    currentRoute.push([lineString.coordinates[i][1], lineString.coordinates[i][0]]);
                //}
                fetch("/api/v1/match/", {
                    method: "POST",
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        route: currentRoute,
                        destination: currentDest,
                        location: current_location,
                        origin_lat: startLat,
                        origin_lon: startLon,
                        destination_lat: endLat,
                        destination_lon: endLon,
                        role: role,
                    })
                })
                .then(res => {
                    if (res.status !== 200) {
                    	if (res.status == 402) {
                    		spinnerBox.style.display = "none";
                			matchesEl.classList.add("flex");
                			errorMessage = `
                				<div class="flex">
                					<p>Your account is not verified!</p>
                					<p>Please go to your dashboard and fill up your profile.</p>
                				</div>
                			`;
                			matchesEl.innerHTML = errorMessage;
                			return;
                    	}
                        throw new Error;
                    }
                    return res.json()
                })
                .then(data => {
                    const id = data.id;
                    data = data.result;
                    spinnerBox.style.display = "none";
                    if (data.length < 1) {
                        matchesEl.innerHTML = "<div class='flex'>No match found!</div>";
                        matchesEl.style.display = "block";
                        return;
                    }
                    
                    matchesEl.innerHTML = `<h3>Match Results</h3>`
                
                    for (let i = 0; i < data.length; i++) {
                        matchesEl.innerHTML += `<div class="match-wrapper">
  							<div class="match-info">
    								<h2>${data[i].username}</h2>
    								<div class="match-details">
      									<div><i class="fas fa-map-marker-alt"></i> ${data[i].origin} - ${data[i].destination}</div>
      									<div><i class="fas fa-percent"></i> ${data[i].match_rate}% match</div>
    								</div>
  							</div>
  							<div class="match-actions">
    								<a href="/profile/${data[i].username}" class="profile-btn">
      									View Profile
    								</a>
    								<a href="/request/?ride_id=${id}&match_id=${data[i].id}" class="request-btn">
      									Request ride
    								</a>
  							</div>
						</div>
						`;
                    }
                    matchesEl.style.display = "block";
                })
                .catch(error => {
                    console.log(error);
                    spinnerBox.style.display = "none";
                   // matchesEl.classList.add("flex");
                    errorMessage = `
                		<div class="flex">
                			<p>Something went wrong!</p>
                			<p>Make sure you have an active internet connection.</p>
                		</div>
                    `;
                    //matchesEl.innerHTML = errorMessage;
                });
        })
        .catch(error => {
        	console.log(error);
                spinnerBox.style.display = "none";
                matchesEl.classList.add("flex");
                errorMessage = `
                		<div class="flex">
                			<p>Something went wrong!</p>
                			<p>Make sure you have an active internet connection.</p>
                		</div>
                `
                matchesEl.innerHTML = errorMessage;
        })
});

function hide(e) {
    searchEl.style.top = '100%';
}

function hideResults(e) {
    resultsEl.style.top = '100%';
    matchesEl.innerHTML = "";
}

personEl.addEventListener('click', () => {
	role = 'passenger';
	searchEl.style.top = '0px';
})

carEl.addEventListener('click', () => {
	role = 'driver';
	searchEl.style.top = '0px';
})
