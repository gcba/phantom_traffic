function log(msg) {
    var d = (new Date).toString();
    console.log(d + ' ' + msg);
    if (msg == 'Mapa cargado') {
        var filename = './BA/' + Date.now().toString();
        page.render(filename + '.gif', {format: 'gif', quality: '100'});
        phantom.exit();
    }
}

var page = require('webpage').create();
page.viewportSize = { width: 4400, height: 5200};
page.onConsoleMessage = function (msg){ log(msg) };

setTimeout(function() {
    log('Timeout exit');
    phantom.exit();
}, 60*1000);

function renderMap() {
    /*
    var s = document.createElement('script');
    s.src = 'https://maps.google.com/maps/api/js?sensor=false';
    document.head.appendChild(s);
    */
    console.log('Insertando mapa');
    var mapDiv = document.createElement('div');
    mapDiv.id = "map";
    mapDiv.style.position = 'absolute';
    mapDiv.style.top = '0';
    mapDiv.style.left = '0';
    mapDiv.style.height = '100%';
    mapDiv.style.width = '100%';
    document.body.appendChild(mapDiv);
    var mapStyles = [{ featureType: "all", stylers: [{ visibility: "off" }] }];
    var latlng = new google.maps.LatLng(-34.6191182, -58.4396684);
    var mapOptions = { center: latlng, zoom: 15, styles: mapStyles };
    var map = new google.maps.Map(document.getElementById("map"), mapOptions);
    var trafficLayer = new google.maps.TrafficLayer();
    trafficLayer.setMap(map);
    google.maps.event.addListenerOnce(map, 'tilesloaded', function () {
        console.log('Mapa cargado');
    });
}

var googleJs = 'https://maps.google.com/maps/api/js?sensor=false';
page.open('about:blank', function (status) {
    if (status == 'success') {
        log('Abriendo pagina en blanco');
        page.includeJs(googleJs, function() {
            log('Lib de googlemaps cargada');
            page.evaluate(renderMap);
        });
    }
});
