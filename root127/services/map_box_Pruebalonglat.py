# -*- coding: utf-8 -*-
from zato.server.service import Service


class MapBox(Service):

    def handle(self):
        self.response.payload = """
        <!DOCTYPE html>
        <html lang="en">
            <head>
                <meta charset="UTF-8">
                <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"
                    integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
                <script src="https://code.jquery.com/jquery-3.3.1.min.js"
                    integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8="
                    crossorigin="anonymous">
                </script>
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <link rel="stylesheet" href="https://unpkg.com/leaflet@1.3.1/dist/leaflet.css"
                    integrity="sha512-Rksm5RenBEKSKFjgI3a41vrjkw4EVPlJ3+OiI65vTjIdo9brlAacEuKOiQ5OFh7cOI1bkDwLqdLw3Zg0cRJAAQ=="
                    crossorigin=""/>
                <script src="https://unpkg.com/leaflet@1.3.1/dist/leaflet.js"
                    integrity="sha512-/Nsx9X4HebavoBvEBuyp3I7od5tA0UzAxs+j83KgC8PU0kgB4XiK4Lfe4y4cgBtaRJQEIFCW+oC506aPT2L1zw=="
                    crossorigin="">
                </script>
                <script src='https://api.tiles.mapbox.com/mapbox.js/plugins/leaflet-omnivore/v0.3.1/leaflet-omnivore.min.js'> 
                </script>
                <style>
                    body { margin:0; padding:0; }
                    #mapid {
                       position:absolute;
          width:100%;
          top:0; /* The height of the header */
          bottom:0;
        left:0;
                    }
                    .margin-left-1rem{
                        margin-left: 1rem;
                    }
                    .padding-left-1rem{
                        padding-left: 1rem;
                    }
                    .padding-left-3rem{
                        padding-left: 3rem;
                    }
                </style>
                <title>Map Box Testing</title>
            </head>
            <body>
            
           
            <style type='text/css'>
                #info {
                    display: block;
                    position: relative;
                    margin: 0px auto;
                    width: 50%;
                    padding: 10px;
                    border: none;
                    border-radius: 3px;
                    font-size: 12px;
                    text-align: center;
                    color: #222;
                    background: #fff;
                }
            </style>
            <div id='mapid'></div> 
            <pre id='info'></pre> 
                <script>

                    function defineDiff() {
                        // Define diff function in arrays
                        Array.prototype.diff = function (a) {
                            return this.filter(function (i) {
                                return a.indexOf(i) === -1;
                            });
                        };
                    }




                    var map = L.map('mapid', {zoomDelta: 0.5,zoomSnap: 0.5}).setView([39.47841096088879, -6.340684443712235], 20);
                    var streets = L.tileLayer('https://api.mapbox.com/styles/v1/mapbox/streets-v10/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1IjoiZmFoYW5pIiwiYSI6ImNqMTZiYm4xMjAyYjEzMnFxdmxnd2V3cHkifQ.-8Hau4tMxMiiSF-9D5AAYA', {maxZoom: 25}).addTo( map );
                    var layers = [];
                    var layersIds = [];

                    var selectedFloor = 0;

                    let pabellonInformatica =
                        {"type": "FeatureCollection", "features": [{"type": "Feature", "properties": {"name": "Pabellón de Informática"},"style" : { "stroke": "#555555", "stroke-width": 2, "stroke-opacity": 1, "fill": "#00aa22", "fill_opacity": 0.5 }, "geometry": { "type": "Polygon", "coordinates": [ [ [ -6.34220372242568, 39.4793228175059 ], [ -6.34187879809926, 39.4792546328079 ], [ -6.34203009098874, 39.4788224029669 ], [ -6.34205598339601, 39.4788278891285 ], [ -6.34214076833743, 39.4785900244351 ], [ -6.34241441554359, 39.478648413043 ], [ -6.34233166137921, 39.4788862775367 ], [ -6.34235755378647, 39.4788909799567 ], [ -6.34220372242568, 39.4793228175059 ] ] ] } } ] };
                    
                    let pabellonTelecomunicaciones=
                        {"type": "FeatureCollection", "features": [{"type": "Feature", "properties": {"name": "Pabellón de Telecomunicaciones"},"style" : { "stroke": "#555555", "stroke-width": 2, "stroke-opacity": 1, "fill": "#00aa22", "fill_opacity": 0.5 }, "geometry": { "type": "Polygon", "coordinates": [ [ [ -6.341727, 39.479218 ], [ -6.341248, 39.4792115 ], [ -6.341429, 39.478684 ], [ -6.341527, 39.478708 ], [ -6.341783, 39.478688 ], [ -6.341555, 39.478639 ], [ -6.341780, 39.478687 ], [ -6.341755, 39.478759 ], [ -6.341813, 39.478770 ] ] ] } } ] };
 
                    let pabellonArquitectura =
                        {"type": "FeatureCollection", "features": [{"type": "Feature", "properties": {"name": "Pabellón de Arquitectura Técnica"},"style" : { "stroke": "#555555", "stroke-width": 2, "stroke-opacity": 1, "fill": "#00aa22", "fill_opacity": 0.5 }, "geometry": { "type": "Polygon", "coordinates": [ [ [ -6.342444925, 39.479340189 ], [ -6.3424557234, 39.4793113646 ], [ -6.342454264, 39.4793110363 ], [ -6.3424555686, 39.4793075537 ], [ -6.3424570281, 39.4793078821 ],[ -6.3424749994, 39.4792599113 ],[ -6.3424735399, 39.4792595829 ],[ -6.3424748225, 39.4792561595 ],[ -6.3424762819, 39.4792564878 ],[ -6.342516673, 39.4791486719 ],[ -6.3425152135, 39.4791483435 ],[ -6.3425164967, 39.4791449183 ],[ -6.3425179561, 39.4791452467 ],[ -6.3425360516, 39.4790969506 ],[ -6.3425345899, 39.4790966217 ],[ -6.342535906, 39.4790931088 ],[ -6.3425373676, 39.4790934376 ],[ -6.3425554593, 39.4790451389 ],[ -6.3425539999, 39.4790448105 ],[ -6.3425552938, 39.4790413566 ],[ -6.3425567532, 39.479041685 ],[ -6.3425749578, 39.4789930913 ],[ -6.3425734983, 39.4789927629 ],[ -6.3425748036, 39.4789892787 ],[ -6.342576263, 39.478989607 ],[ -6.3425868884, 39.4789612446 ],[ -6.3426086484, 39.4789661403 ],[ -6.3426177789, 39.4789417681 ],[ -6.3426158014, 39.4789413232 ],[ -6.3426170249, 39.4789380573 ],[ -6.3426190024, 39.4789385022 ],[ -6.3426377316, 39.4788885077 ],[ -6.3426357541, 39.4788880628 ],[ -6.3426370594, 39.4788845785 ],[ -6.3426390362, 39.4788850251 ],[ -6.3426572192, 39.4788364888 ],[ -6.3426552417, 39.4788360439 ],[ -6.3426565533, 39.4788325426 ],[ -6.3426585308, 39.4788329875 ],[ -6.3426686752, 39.4788059088 ],[ -6.3427002488, 39.4788130124 ],[ -6.3427108011, 39.4787848447 ],[ -6.3426792275, 39.4787777411 ],[ -6.3426970912, 39.4787300566 ],[ -6.3427783154, 39.4787483308 ],[ -6.3427847947, 39.4787310353 ], [ -6.3429004149, 39.4787570479 ],[ -6.3428939356, 39.4787743434 ], [ -6.3429770701, 39.4787930472 ],[ -6.3429592065, 39.4788407317 ],[ -6.3429266588, 39.4788334091 ],[ -6.3429161066, 39.4788615768 ],[ -6.3429486543, 39.4788688995 ],[ -6.3429385145, 39.4788959665 ],[ -6.3429398923, 39.4788962765 ],[ -6.3429385763, 39.4788997895 ],[ -6.3429371984, 39.4788994795 ],[ -6.3429190163, 39.4789480142 ],[ -6.3429203942, 39.4789483242 ], [ -6.3429190889, 39.4789518084 ],[ -6.3429177111, 39.4789514984 ],[ -6.3428990524, 39.479001305 ],[ -6.3429004303, 39.479001615 ],[ -6.3428991364, 39.4790050689 ],[ -6.3428977585, 39.4790047589 ],[ -6.3428886282, 39.4790291311 ],[ -6.3429103041, 39.4790340078 ],[ -6.3429109462, 39.4790341523 ],[ -6.342900321, 39.4790625148 ],[ -6.3429017827, 39.4790628436 ],[ -6.3429004774, 39.4790663278 ],[ -6.3428990158, 39.479065999 ],[ -6.3428808114, 39.4791145928 ],[ -6.3428822731, 39.4791149216 ],[ -6.3428809792, 39.4791183755 ],[ -6.3428795289, 39.4791180163 ],[ -6.3428614239, 39.479166345 ],[ -6.3428628855, 39.4791666738 ],[ -6.3428615695, 39.4791701868 ],[ -6.3428601078, 39.4791698579 ],[ -6.3428420148, 39.4792181546 ],[ -6.3428434764, 39.4792184834 ],[ -6.3428421933, 39.4792219086 ],[ -6.3428407316, 39.4792215798 ],[ -6.3428296958, 39.4792510381 ],[ -6.34277457, 39.4792386358 ],[ -6.3427553264, 39.4792900035 ],[ -6.3428104522, 39.4793024058 ],[ -6.342800341, 39.4793293959 ],[ -6.3428018027, 39.4793297247 ],[ -6.3428005202, 39.4793331482 ],[ -6.3427990585, 39.4793328193 ],[ -6.3427810874, 39.4793807902 ],[ -6.3427825491, 39.479381119 ],[ -6.3427812444, 39.4793846016 ],[ -6.3427797828, 39.4793842727 ],[ -6.3427689844, 39.4794130971 ],[ -6.342688373, 39.4793949609 ],[ -6.3426879493, 39.479396092 ],[ -6.3426834532, 39.4793950804 ],[ -6.342683877, 39.4793939494 ],[ -6.3426562777, 39.47938774 ],[ -6.3426529084, 39.4793967337 ],[ -6.3426146328, 39.4793881223 ],[ -6.3426178459, 39.4793795456 ],[ -6.3425956393, 39.4793745495 ],[ -6.3425924262, 39.4793831262 ],[ -6.3425541506, 39.4793745148 ],[ -6.3425575199, 39.4793655211 ],[ -6.3425276471, 39.4793588002 ],[ -6.3425272234, 39.4793599313 ],[ -6.3425227295, 39.4793589202 ],[ -6.3425231532, 39.4793577892 ],[ -6.342444925, 39.479340189 ] ] ] } } ] };




                    //omnivore.wkt.parse('POLYGON ((-6.3423514 39.4788871, -6.3423313 39.4788840, -6.3424104 39.4786418, -6.3421436 39.4785921, -6.3420510 39.4788261, -6.3420296 39.4788209, -6.3418753 39.4792484, -6.3421945 39.4793209, -6.3423514 39.4788871))').addTo(map);
                

        /*
                    let geojsonFile =
                        {"type": "FeatureCollection", "features": [{"type": "Feature", "properties": {"name": "Sensor agua, temperatura co2"},"style" :
                                    { "stroke": "#555555", "stroke-width": 2, "stroke-opacity": 1, "fill": "#8000ff", "fill_opacity": 0.5 }, "geometry":
                                    { "type": "Point", "coordinates": [-6.34222452058909, 39.4790276756012] }}]};

                    layers[0] =
                        L.geoJSON(geojsonFile,
                            {
                                style: function(feature) {
                                    return {
                                        color: feature.style.fill,
                                        fillOpacity: feature.style.fill_opacity
                                    };
                                },
                                onEachFeature: function (feature, layer) {

                                    if (feature.properties && feature.properties.name) {
                                        layer.bindPopup(feature.properties.name+"");
                                    }
                                }
                            }
                        );
                    layers[0].addTo(map);
        */

                    /*let marker = L.marker([39.4788871, -6.3423]).addTo(map);
                    marker.bindPopup("" +
                        "<iframe   src=\"http://localhost/zm/cgi-bin/nph-zms?mode=jpeg&scale=100&maxfps=5&buffer=1000&monitor=23&auth=3ab4cd3e0adf723c95c02ab742dc535f&connkey=539793&rand=1525860427\">\n" +

                        "</iframe >" +
                        "").openPopup();
                    */

                    //map.on('zoomend moveend', function onDragEnd(s){
                      map.on('moveend', function onDragEnd(s){
                          console.log(map.getZoom());
                        //alert(map.getBounds().toBBoxString());

                        queryNeo4j();


                    });

                    defineFloorControl();


                    function queryNeo4j() {

                         //var statement = "CALL spatial.bbox('geom',{lon:"+map.getBounds().getWest()+", lat:"+map.getBounds().getSouth()+"}, {lon:"+map.getBounds().getEast()+", lat:"+map.getBounds().getNorth()+"});";
                        let statement = "WITH 'POLYGON(("+map.getBounds().getNorthWest().lng+" "+map.getBounds().getNorthWest().lat+
                            ", "+map.getBounds().getNorthEast().lng+" "+map.getBounds().getNorthEast().lat+
                            ", "+map.getBounds().getSouthEast().lng+" "+map.getBounds().getSouthEast().lat+
                            ", "+map.getBounds().getSouthWest().lng+" "+map.getBounds().getSouthWest().lat+
                            ", "+map.getBounds().getNorthWest().lng+" "+map.getBounds().getNorthWest().lat+"))' as polygon " +
                            "CALL spatial.intersects('geom',polygon) YIELD node " +
                            //"MATCH (node) WHERE node.enable_in_zoom <= "+map.getZoom()+" " + " AND node.disable_in_zoom >=" + map.getZoom() + " " +
                            "MATCH (node)-[*0..]-(Floor)" +
                            " RETURN *";

                        console.log(statement);
                        


                        $.ajaxSetup({
                            headers: {
                                "Authorization": 'Basic ' + window.btoa("Smart:Politech"),
                                //"Authorization": 'Basic ' + window.btoa("neo4j:opticalflow"),
                                "X-Stream": true,
                                "Accept": "application/json; charset=UTF-8",
                                "Content-Type": "application/json"
                            }
                        });
                        $.ajax({
                            //url: "http://nicolas.unex.es:7474/db/data/transaction/commit",
                            url: "http://158.49.112.122:7474/db/data/transaction/commit",
                            type: "POST",
                            data: JSON.stringify({
                                statements: [{
                                    statement: statement,
                                    resultDataContents: ["row", "graph", "rest"]
                                    //parameters: params || {},

                                }]
                            }),
                            dataType: "json",
                            contentType: "application/json;charset=UTF-8",
                            error: function(err) {
                                alert("error");
                            },
                            success: function(res) {

                                console.log(res);
                                processNodes(res.results[0].data);
                            }
                        });
                    }


                    function defineFloorControl() {
                        var legend = L.control({position: 'topright'});
                        legend.onAdd = function (map) {
                            var div = L.DomUtil.create('div', 'info legend');
                            div.innerHTML = '<select onchange="selectFloor(this);return false;"><option value="0">Planta 0</option><option value="1">Planta 1</option></select>';
                            div.firstChild.onmousedown = div.firstChild.ondblclick = L.DomEvent.stopPropagation;
                            return div;
                        };
                        legend.addTo(map);
                    }

                    function selectFloor(data) {
                        //console.log($(data).val());
                        selectedFloor = $(data).val();
                        queryNeo4j();
                    }



                    function removeNodes(nodesToRemove) {

                        nodesToRemove.forEach(function(nodeToRemove) {
                            map.removeLayer(layers[nodeToRemove]);
                            delete layers[nodeToRemove];

                            let index = layersIds.indexOf(nodeToRemove);
                            if (index > -1) {
                                layersIds.splice(index, 1);
                            }
                        });

                    }

                    function processNodes(nodes) {

                       defineDiff();

                        // Collect the ids of the building nodes that matches the spatial query
                        let matchedNodes = [];
                        let nodesToDraw = [];
                        nodes.forEach(function(node) {
                            //console.log(node);
                            //console.log(node.row[0].id);
                            //console.log(node.row[0].min_zoom);

                            // Add it is between the zoom
                            if(node.row[0].min_zoom<=map.getZoom() && map.getZoom()<=node.row[0].max_zoom){
                                //console.log(node.row[0].id);


                                // If it is a floor, add only the selected ones
                                if(node.rest[0].metadata.labels[0] == "Floor"){	
                                    if (node.row[0].id == "UEXCC_TEL_P0"+selectedFloor || node.row[0].id == "UEXCC_INF_P0"+selectedFloor  ) {
                                        matchedNodes.push(node.row[0].id);
                                        nodesToDraw[node.row[0].id] = node.row[0];
                                    }

                                } else if(node.rest[0].metadata.labels[0] == "Building") {
                                    matchedNodes.push(node.row[0].id);
                                    nodesToDraw[node.row[0].id] = node.row[0];
                                } else if (selectedFloor == 0 ) {
                                    console.log(node.row[0].id.substring(0,12))
                                    if (node.row[0].id.substr(0,13)== "UEXCC_TEL_P0"+selectedFloor ||  node.row[0].id.substr(0,13) == "UEXCC_INF_P0"+selectedFloor){
                                        console.log('entra')
                                        matchedNodes.push(node.row[0].id);
                                        nodesToDraw[node.row[0].id] = node.row[0];
                                    }    
                                } else if (selectedFloor == 1 ){
                                    if (node.row[0].id.substr(0,13)== "UEXCC_TEL_P0"+selectedFloor ||  node.row[0].id.substr(0,13) == "UEXCC_INF_P0"+selectedFloor){
                                        matchedNodes.push(node.row[0].id);
                                        nodesToDraw[node.row[0].id] = node.row[0];
                                    }    
                                }



                            }
                            else {
                                //console.log("NO");
                            }
                        });


                        let nodesToRemove = layersIds.diff(matchedNodes);
                        //console.log("Nodes to remove: ");
                        //console.log(nodesToRemove);
                        removeNodes(nodesToRemove);


                        //console.log("Nodes to draw: ");
                        //console.log(nodesToDraw);
                        //console.log("Nodes to add: ");
                        //console.log(matchedNodes);
                        matchedNodes.forEach(function(nodeToAdd) {

                            // add it if the node doesn't exist in the map
                            if (!layers[nodeToAdd])
                            {

                                // add it if the node has the geojson property
                                if(nodesToDraw[nodeToAdd].geojson){




                                    //console.log("El nodo "+ nodeToAdd+ " no existe, lo añado");
                                    layersIds.push(nodeToAdd);
                                    layers[nodeToAdd] = L.geoJSON(JSON.parse(nodesToDraw[nodeToAdd].geojson),
                                        {
                                            pointToLayer: function (feature, latlng) {
                                                if (nodesToDraw[nodeToAdd].img)
                                                {
                                                    let icon = L.icon({iconUrl: nodesToDraw[nodeToAdd].img});
                                                    return L.marker(latlng,  {icon: icon});
                                                } else {
                                                    return L.marker(latlng);
                                                }
                                            },
                                            style: function(feature) {
                                                return {
                                                    color: feature.style.fill ? feature.style.fill : '#3388ff',
                                                    fillOpacity: feature.style.fill_opacity ? feature.style.fill_opacity : 0.4,
                                                    width: 2

                                                };
                                            },
                                            onEachFeature: function (feature, layer) {

                                                let bindText = "";

                                                if (nodesToDraw[nodeToAdd].dataSource){
                                                    bindText = bindText + "" + nodesToDraw[nodeToAdd].dataSource + "<br> <a href='"+$(nodesToDraw[nodeToAdd].dataSource)[0].src+"' target='_blank'>Abrir en ventana</a>" ;


                                                }
                                                else if (feature.properties && feature.properties.name)
                                                    bindText = bindText + "" + feature.properties.name + "<br>" + nodesToDraw[nodeToAdd].id;

                                                 layer.bindPopup(bindText);

                                            }
                                        });

                                    layers[nodeToAdd].addTo(map);
                                }
                                else
                                {
                                    //console.log("El nodo "+ nodeToAdd+ ",no tiene geojosn");
                                }

                            }
                            else
                            {
                                //console.log("El nodo "+ nodeToAdd+ " existe, no lo añado");
                            }
                        });

                        
                    }
                    console.log("Las capas que tenemos en total son:");
                    console.log(layers);
                map.on('mousemove', function (e) {
                    document.getElementById('info').innerHTML =
                        // e.point is the x, y coordinates of the mousemove event relative
                        // to the top-left corner of the map
                        JSON.stringify(e.point) + '<br />' +
                        // e.lngLat is the longitude, latitude geographical position of the event
                        JSON.stringify(e.latlng.wrap());
                });
                </script>
            </body>
        </html>"""

        self.response.content_type = 'text/html; charset=utf-8'