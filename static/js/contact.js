mapboxgl.accessToken = 'pk.eyJ1IjoiaG9ycGVhenkiLCJhIjoiY2xmNjFuOGJyMWk0bzN2cjBzZno0NXNmdCJ9.aEgc6K_vrA2mctaeIFzBrg';

// Create a new Mapbox map
const map = new mapboxgl.Map({
    container: 'map',
    projection: 'globe',
    style: 'mapbox://styles/horpeazy/clf7ms36k001c01qoerxs6zdt',
    center: [5.62575, 6.33815],
    zoom: 8,
});

// Add a marker to the map
let marker = new mapboxgl.Marker()
    .setLngLat([5.62575, 6.33815])
    .addTo(map);