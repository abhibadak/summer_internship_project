document.getElementById('getLocation').addEventListener('click', function() {
    if (!navigator.geolocation) {
        document.getElementById('location-info').innerHTML = 
            "Geolocation is not supported by your browser.";
        return;
    }
    
    document.getElementById('location-info').innerHTML = "Locating...";
    
    navigator.geolocation.getCurrentPosition(
        function(position) {
            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;
            const accuracy = position.coords.accuracy;
            
            document.getElementById('location-info').innerHTML = `
                <strong>Latitude:</strong> ${latitude}<br>
                <strong>Longitude:</strong> ${longitude}<br>
                <strong>Accuracy:</strong> ±${accuracy} meters<br>
                <strong>Timestamp:</strong> ${new Date(position.timestamp).toLocaleString()}
            `;
            
            showOnMap(latitude, longitude);
        },
        function(error) {
            let errorMessage;
            switch(error.code) {
                case error.PERMISSION_DENIED:
                    errorMessage = "User denied the request for Geolocation.";
                    break;
                case error.POSITION_UNAVAILABLE:
                    errorMessage = "Location information is unavailable.";
                    break;
                case error.TIMEOUT:
                    errorMessage = "The request to get user location timed out.";
                    break;
                case error.UNKNOWN_ERROR:
                    errorMessage = "An unknown error occurred.";
                    break;
            }
            document.getElementById('location-info').innerHTML = errorMessage;
        },
        {
            enableHighAccuracy: true,
            timeout: 10000,
            maximumAge: 0
        }
    );
});

function showOnMap(lat, lng) {
    const mapElement = document.getElementById('map');
    
    if (typeof google !== 'undefined') {
        const location = { lat: lat, lng: lng };
        const map = new google.maps.Map(mapElement, {
            zoom: 15,
            center: location
        });
        new google.maps.Marker({
            position: location,
            map: map,
            title: "Your Location"
        });
    } else {
        mapElement.innerHTML = 
            `<p>To show the map, please include Google Maps API.</p>
             <p>Latitude: ${lat}, Longitude: ${lng}</p>`;
    }
}