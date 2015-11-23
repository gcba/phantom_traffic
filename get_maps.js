var args      = require('system').args;

var m_folder  = args[1];
var m_width   = args[2];
var m_height  = args[3];
var m_zoom    = args[4];
var m_format  = args[5];
var m_quality = args[6];
var m_lat     = args[7];
var m_lon     = args[8];
var m_name    = args[9]

function log(msg) {
    var d = (new Date).toString();
    console.log(d + ' ' + msg);
    if (msg == 'Mapa cargado!') {
        var filename = './'+m_folder+'/' + Date.now().toString();
        console.log('Renderizando mapa de '+m_name)
        page.render(filename + '.'+m_format, {format: m_format, quality: m_quality});
        console.log('DONE!')
        phantom.exit();
    }
}

var page = require('webpage').create();
page.viewportSize = { width: m_width, height: m_height};
page.onConsoleMessage = function (msg){ log(msg) };

setTimeout(function() {
    log('Timeout exit');
    phantom.exit();
}, 60*1000);

function renderMap(lat,lon,zoom) {
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
            page.evaluate(renderMap,m_lat,m_lon, parseInt(m_zoom));
        });
    }
});

