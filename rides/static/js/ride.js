const searchInput = document.querySelector(".destination");
const locations = document.querySelector(".locations");
const locationItems = document.querySelectorAll(".location");
const searchEl = document.querySelector('.search');
const resultEl = document.querySelector(".match-result");
const resultsWrapper = document.querySelector('.results-wrapper');
const personEl = document.querySelector('.fa-person');
const carEl = document.querySelector('.fa-car');
const matchBtn = document.querySelector('.fa-search');
let zoomed, dMarker, endLon, endLat, startLat, startLon;
let currenRoute, currentDest, current_location;
let role;
const center = [8.6753, 9.0820];

mapboxgl.accessToken = 'pk.eyJ1IjoiaG9ycGVhenkiLCJhIjoiY2xmNjFuOGJyMWk0bzN2cjBzZno0NXNmdCJ9.aEgc6K_vrA2mctaeIFzBrg';

// Create a new Mapbox map
const map = new mapboxgl.Map({
    container: 'map',
    projection: 'globe',
    style: 'mapbox://styles/horpeazy/clf7ms36k001c01qoerxs6zdt',
    center: center,
    zoom: 15,
});
    
map.addControl(new mapboxgl.NavigationControl(), 'top-left');


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

        // Create a GeoJSON object from the route geometry
        const routeGeoJSON = {
            type: 'Feature',
            properties: {},
            geometry: route.geometry,
        };

        // Add the route layer to the map
        const source = map.getLayer('source')
        if (source) {
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
		if (!endLat || !endLon) {
        	alert("Please select a destination as driver or passenger.")
        	return;
    	}
        routeUrl = "https://router.project-osrm.org/route/v1/driving/";
        showResults();
        resultEl.innerHTML = `<div class="spinner">
  							  	<div class="circle"></div>
							  </div>
							 `
        fetch(routeUrl + startLon + ',' + startLat + ';' + endLon + ',' + endLat + '?geometries=geojson')
        .then(function (response) {
            return response.json();
        })
        .then(function (json) {
            // Parse the response and create a LatLng array for the route
            const route = json.routes[0];
            const lineString = route.geometry;
            currentRoute = [];
            for (var i = 0; i < lineString.coordinates.length; i++) {
                currentRoute.push([lineString.coordinates[i][1], lineString.coordinates[i][0]]);
            }
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
                if (res.status == 200) {
                    return res.json()
                } else if ( res.status == 401) {
                	resultEl.innerHTML = `
                							<div class='flex'>
                								Please verify your profile by completing it before you can ride!
                							</div>`;
                }
                throw new Error;
            })
            .then(data => {
                resultEl.innerHTML = "";
                const id = data.id;
                data = data.result;
                if (data.length < 1) {
                    resultEl.innerHTML = "<div class='flex'>No match found!</div>";
                    return;
                }
            
                for (let i = 0; i < data.length; i++) {
                   resultEl.innerHTML += `<div class="match-wrapper">
  					<div class="match-info">
  						<div>
  						  <img src="${data[i].profile_picture}" alt="" />
  						  <div>
  						    <h2>${data[i].username}</h2>
  						    <div>
  						      <i class="fa fa-star"></i>
  						      <span>${data[i].user_rating}</span>
  						      <i class="fa fa-${data[i].role == 'driver' ? 'car' : 'person'}"></i>
  						    </div>
  						  </div>
  						</div>
    						<div class="match-details">
      							<div><i class="fas fa-map-marker-alt"></i>${data[i].origin} --- ${data[i].destination}</div>
      						</div>
      						<div class="match-details">
      							<div><i class="fas fa-sync"></i>Match rate ${data[i].match_rate}%</div>
      						</div>
    					</div>
    					<div class="match-actions" style="float: right;">
    						<a href="/profile/${data[i].username}" class="profile-btn">
      							View Profile
    						</a>
    						<a href="/request/?ride_id=${data[i].ride_id}&match_id=${data[i].id}" class="profile-btn">
      							Request
    						</a>
					</div>
  			</div>`
                }
            })
            .catch(error => {
                console.log(error);
                resultEl.innerHTML = "<div class='flex'>Ooops! Something went wrong.<br> Please try again.</div>";
            });
        });
    });
    
function showResults() {
    resultsWrapper.style.top = '20vh';
}

function hide(e) {
    searchEl.style.top = '100%';
}

function hideResults() {
    resultsWrapper.style.top = '100%';
}

personEl.addEventListener('click', () => {
	role = 'passenger';
	searchEl.style.top = '0px';
	searchEl.style.display = 'block';
})

carEl.addEventListener('click', () => {
	role = 'driver';
	searchEl.style.top = '0px';
	searchEl.style.display = 'block';
})
