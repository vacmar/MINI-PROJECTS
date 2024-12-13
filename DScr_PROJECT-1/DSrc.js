// Include the necessary Leaflet and OpenRouteService libraries
// Ensure these scripts are included in your HTML file
// <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
// <script src="https://unpkg.com/leaflet-routing-machine@3.2.12/dist/leaflet-routing-machine.js"></script>
// <script src="https://unpkg.com/leaflet-control-geocoder/dist/Control.Geocoder.js"></script>
// <script src="https://unpkg.com/leaflet-routing-openrouteservice/dist/leaflet-routing-openrouteservice.js"></script>

// Initialize the Leaflet map
let map = L.map('map').setView([51.505, -0.09], 13);

// Add OpenStreetMap tiles to the map
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Array to store the coordinates of the source and destination
let points = [];
let markers = [];
let control = null;

// Map click event to select source and destination
map.on('click', function(e) {
    let latLng = e.latlng;
    points.push([latLng.lat, latLng.lng]);

    // Add a marker at the clicked location
    let marker = L.marker(latLng).addTo(map);
    markers.push(marker);

    if (points.length === 1) {
        alert("Source selected. Now click to select the destination.");
    } else if (points.length === 2) {
        alert("Destination selected. Drawing the shortest path...");
        console.log("Calling drawPath function");
        drawPath();
    } else {
        alert("Both source and destination are already selected. Reset the map to choose new points.");
    }
});

// Function to draw the path between the selected source and destination
function drawPath() {
    if (points.length === 2) {
        console.log("Points array:", points);
        control = L.Routing.control({
            waypoints: [
                L.latLng(points[0][0], points[0][1]),
                L.latLng(points[1][0], points[1][1])
            ],
            router: L.Routing.openrouteservice({
                serviceUrl: 'https://api.openrouteservice.org/v2/directions/driving-car',
                apiKey: '5b3ce3597851110001cf62486e397feae85945b785e5b8e4e8b304ec'
            }),
            geocoder: L.Control.Geocoder.nominatim(),
            lineOptions: {
                styles: [
                    {color: 'blue', opacity: 0.8, weight: 6}
                ]
            }
        }).addTo(map);

        control.on('routesfound', function(e) {
            console.log("Routes found:", e.routes);
        });

        control.on('routingerror', function(e) {
            console.error("Routing error:", e);
        });
    }
}

// Function to reset the map
function resetMap() {
    points = [];

    // Remove all markers
    markers.forEach(marker => map.removeLayer(marker));
    markers = [];

    // Remove the route (control)
    if (control) {
        map.removeControl(control);
        control = null;
    }

    alert("Map has been reset. Please select a new source and destination.");
}
