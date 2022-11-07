# -*- coding: utf-8 -*-
from zato.server.service import Service


class Ecogram(Service):

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
                <script src='https://api.tiles.mapbox.com/mapbox.js/plugins/leaflet-omnivore/v0.3.1/leaflet-omnivore.min.js'></script>
                <style>
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
                <div id='mapid'></div>
                <script>

                    function defineDiff() {
                        // Define diff function in arrays
                        Array.prototype.diff = function (a) {
                            return this.filter(function (i) {
                                return a.indexOf(i) === -1;
                            });
                        };
                    }




                    var map = L.map('mapid', {zoomDelta: 0.5,zoomSnap: 0.5}).setView([-34.09385187545587, -54.868589530032374], 13);
                    var streets = L.tileLayer('https://api.mapbox.com/styles/v1/mapbox/streets-v10/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1IjoiZmFoYW5pIiwiYSI6ImNqMTZiYm4xMjAyYjEzMnFxdmxnd2V3cHkifQ.-8Hau4tMxMiiSF-9D5AAYA', {maxZoom: 25}).addTo( map );
                    var layers = [];
                    var layersIds = [];

                    var selectedFloor = 0;


                    map.on('moveend', function onDragEnd(s){
                        console.log(map.getZoom());
                        //alert(map.getBounds().toBBoxString());

                        queryNeo4j();
                    });

                    queryNeo4j();


                    function queryNeo4j() {

                         //var statement = "CALL spatial.bbox('geom',{lon:"+map.getBounds().getWest()+", lat:"+map.getBounds().getSouth()+"}, {lon:"+map.getBounds().getEast()+", lat:"+map.getBounds().getNorth()+"});";
                        let statement = "WITH 'POLYGON(("+map.getBounds().getNorthWest().lng+" "+map.getBounds().getNorthWest().lat+
                            ", "+map.getBounds().getNorthEast().lng+" "+map.getBounds().getNorthEast().lat+
                            ", "+map.getBounds().getSouthEast().lng+" "+map.getBounds().getSouthEast().lat+
                            ", "+map.getBounds().getSouthWest().lng+" "+map.getBounds().getSouthWest().lat+
                            ", "+map.getBounds().getNorthWest().lng+" "+map.getBounds().getNorthWest().lat+"))' as polygon " +
                            "CALL spatial.intersects('geom',polygon) YIELD node as fincas " + 
                            "OPTIONAL MATCH (fincas)<-[:PARCELA_DE]-(parcelas:Parcela) " + 
                            "OPTIONAL MATCH (parcelas)<-[:ALAMBRE_DE]-(alambres:Alambre) " +
                            "OPTIONAL MATCH (parcelas)<-[:CHARCA_DE]-(charcas:Charca) " +
                            "OPTIONAL MATCH (parcelas)<-[:EDIFICIO_DE]-(edificios:Edificio) " +
                            "RETURN fincas, parcelas, alambres, charcas, edificios";
                            //"RETURN *";

                        console.log(statement);


                        $.ajaxSetup({
                            headers: {
                                //"Authorization": 'Basic ' + window.btoa("Smart:Politech"),
                                "Authorization": 'Basic ' + window.btoa("neo4j:eco4j"),
                                "X-Stream": true,
                                "Accept": "application/json; charset=UTF-8",
                                "Content-Type": "application/json"
                            }
                        });
                        $.ajax({
                            //url: "http://nicolas.unex.es:8080/db/data/transaction/commit",
                            url: "http://ecogramapp.org:8080/db/data/transaction/commit",
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

                            node.graph.nodes.forEach(function(nodeGraph) {

                                // Add it is between the zoom and it isn't in the matchedNodes already
                                if(nodeGraph.properties.min_zoom<=map.getZoom() && map.getZoom()<=nodeGraph.properties.max_zoom && !matchedNodes.includes(nodeGraph.id)){
                                    matchedNodes.push(nodeGraph.id);
                                    nodesToDraw[nodeGraph.id] = nodeGraph.properties;
                                }
                                else {
                                    //console.log("NO");
                                }

                            });
                        });

                        let nodesToRemove = layersIds.diff(matchedNodes);

                        //console.log(matchedNodes);
                        //console.log(nodesToRemove);
                        //console.log(layers);
                        //console.log(nodesToDraw);


                        removeNodes(nodesToRemove);

                        //console.log(matchedNodes);

                        //matchedNodes.sort(function(a, b) {
                        //	return parseFloat(a.z_index) - parseFloat(b.z_index);
                        //});


                        console.log(matchedNodes);

                        matchedNodes.forEach(function(nodeToAdd) {

                            // add it if the node doesn't exist in the map
                            if (!layers[nodeToAdd])
                            {

                                // add it if the node has the geojson property
                                if(nodesToDraw[nodeToAdd].geojson){

                                    var paneZIndex = map.createPane(nodesToDraw[nodeToAdd].z_index+"");

                                    map.getPane(nodesToDraw[nodeToAdd].z_index+"").style.zIndex = nodesToDraw[nodeToAdd].z_index+200;
                                    console.log(map.getPane(nodesToDraw[nodeToAdd].z_index+"").style.zIndex);

                                    //console.log("El nodo "+ nodeToAdd+ " no existe, lo añado");
                                    layersIds.push(nodeToAdd);
                                    layers[nodeToAdd] = L.geoJSON(JSON.parse(nodesToDraw[nodeToAdd].geojson),
                                        {
                                            style: function(feature) {
                                                return {
                                                    color: feature.style.fill ? feature.style.fill : '#3388ff',
                                                    fillOpacity: feature.style.fill_opacity ? feature.style.fill_opacity : 0.4,
                                                    width: 2

                                                };
                                            },
                                            onEachFeature: function (feature, layer) {

                                                let bindText = "";

                                                if (feature.properties && feature.properties.nombre)
                                                    bindText = bindText + "" + feature.properties.nombre;

                                                 layer.bindPopup(bindText);
                                            },
                                            pane: nodesToDraw[nodeToAdd].z_index+""
                                        });

                                    map.addLayer(layers[nodeToAdd]);
                                    //layers[nodeToAdd].addTo(map, {pane: '3'});
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



                        //console.log("Las capas que tenemos en total son:");
                        console.log(map.getPanes());
                    }


                </script>
            </body>
        </html>"""

        self.response.content_type = 'text/html; charset=utf-8'
