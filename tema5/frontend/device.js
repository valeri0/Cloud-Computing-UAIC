function getDevicesData() {
    var xhr = new XMLHttpRequest();

    xhr.addEventListener("readystatechange", function () {
        if (this.readyState === 4) {
            let devices = JSON.parse(this.responseText);
            generateMap(devices);
        }
    });

    xhr.open("GET", "http://127.0.0.1:5000/devices");
    xhr.setRequestHeader("content-type", "application/json");
    xhr.send();
}


function generateMap(data) {
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 4,
        center: {
            lat: 47.151726,
            lng: 27.587914
        }
    });

    var infowindow = new google.maps.InfoWindow();
    var marker, i;

    for (i = 0; i < data.length; i++) {
        if (data[i].hasOwnProperty('location') && data[i].hasOwnProperty('tags') && data[i].hasOwnProperty('value')) {
            var position = {
                lat: data[i].location.lat,
                lng: data[i].location.lon
            };
            var details = '<div><h1>' + data[i].tags[0] + '</h1><h2>Provider: ' + data[i].location.provider + '</h2>' + '<p>Temp: <b>' + data[i].value.temp + '</b>  Pressure: <b>' + data[i].value.pressure + '</b> Connector: <b>' + data[i].metadata.connector + '</b></p></div>';

            marker = new google.maps.Marker({
                position: position,
                map: map
            });

            google.maps.event.addListener(marker, 'click', (function (marker, i) {
                return function () {
                    infowindow.setContent(details);
                    infowindow.open(map, marker);
                }
            })(marker, i));
        }
    }
}
