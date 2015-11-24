var args = require('system').args;

var city_folder = args[1];
var city_width = args[2];
var city_height = args[3];
var city_zoom = args[4];
var img_format = args[5];
var img_quality = args[6];
var city_lat = args[7];
var city_lon = args[8];
var city_name = args[9];

function log(msg) {
    var d = (new Date).toString();
    console.log(d + ' ' + msg);
    if (msg == 'Mapa cargado!') {
        console.log('Renderizando mapa de '+ city_name);
        var filename = './' + city_folder + '/' + Date.now().toString() + '.' + img_format;
        page.render(filename, {format: img_format, quality: img_quality});
        console.log('DONE!');
        phantom.exit();
    }
}

var page = require('webpage').create();
page.viewportSize = { width: city_width, height: city_height};
page.onConsoleMessage = function (msg){ log(msg) };

setTimeout(function() {
    log('Timeout exit');
    phantom.exit();
}, 60*1000);

function renderMap(lat, lon, zoom) {
    console.log('Insertando mapa...');
    var mapDiv = document.createElement('div');
    mapDiv.id = "map";
    mapDiv.style.position = 'absolute';
    mapDiv.style.top = '0';
    mapDiv.style.left = '0';
    mapDiv.style.height = '100%';
    mapDiv.style.width = '100%';
    document.body.appendChild(mapDiv);
    var mapStyles = [{ featureType: "all", stylers: [{ visibility: "off" }] }];
    var latlng = new google.maps.LatLng(lat, lon);
    var mapOptions = { center: latlng, zoom: zoom, styles: mapStyles };
    var map = new google.maps.Map(document.getElementById("map"), mapOptions);
    var trafficLayer = new google.maps.TrafficLayer();
    trafficLayer.setMap(map);
    google.maps.event.addListenerOnce(map, 'tilesloaded', function () {
        console.log('Mapa cargado!');
    });
}

var googleJs = 'https://maps.google.com/maps/api/js?sensor=false';
page.open('about:blank', function (status) {
    if (status == 'success') {
        log('Abriendo pagina en blanco');
        page.includeJs(googleJs, function() {
            log('Lib de googlemaps cargada');
            page.evaluate(renderMap, city_lat, city_lon, parseInt(city_zoom));
        });
    }
});

