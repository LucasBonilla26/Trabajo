#!/usr/bin/env python
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
        integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8=" crossorigin="anonymous">
        </script>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.3.1/dist/leaflet.css"
        integrity="sha512-Rksm5RenBEKSKFjgI3a41vrjkw4EVPlJ3+OiI65vTjIdo9brlAacEuKOiQ5OFh7cOI1bkDwLqdLw3Zg0cRJAAQ=="
        crossorigin="" />
    <script src="https://unpkg.com/leaflet@1.3.1/dist/leaflet.js"
        integrity="sha512-/Nsx9X4HebavoBvEBuyp3I7od5tA0UzAxs+j83KgC8PU0kgB4XiK4Lfe4y4cgBtaRJQEIFCW+oC506aPT2L1zw=="
        crossorigin=""></script>
    <script src="http://158.49.112.127:11223/sidebar_leaflet_js"></script>
    <link rel="stylesheet" href="http://158.49.112.127:11223/sidebar_leaflet_css" />
    <link href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet">
    <script
        src='https://api.tiles.mapbox.com/mapbox.js/plugins/leaflet-omnivore/v0.3.1/leaflet-omnivore.min.js'></script>
    <script type="text/javascript" src="http://158.49.112.127:11223/zlibjs"></script>
    <script type="text/javascript" src="https://cdn.jsdelivr.net/npm/@turf/turf@5/turf.min.js"></script>
    <style>
        #mapid {
            position: absolute;
            width: 100%;
            top: 0;
            /* The height of the header */
            bottom: 0;
            left: 0;
        }

        .margin-left-1rem {
            margin-left: 1rem;
        }

        .padding-left-1rem {
            padding-left: 1rem;
        }

        .padding-left-3rem {
            padding-left: 3rem;
        }
    </style>
    <title>Map Box Testing</title>
</head>

<body>
    <div id='mapid'></div>

    <div id="sidebar" class="sidebar collapsed ">
        <!-- Nav tabs -->
        <div class="sidebar-tabs">
            <ul role="tablist">
                <li><a href="#home" role="tab"><i class="fa fa-bars"></i></a></li>
                <li><a href="#search" role="tab"><i class="fa fa-search"></i></a></li>
            </ul>

            <ul role="tablist">
                <li><a href="#settings" role="tab"><i class="fa fa-gear"></i></a></li>
            </ul>
        </div>

        <!-- Tab panes -->
        <div class="sidebar-content">
            <div class="sidebar-pane" id="home">
                <h1 class="sidebar-header">
                    Filtros
                    <span class="sidebar-close"><i class="fa fa-caret-right"></i></span>
                </h1>
                <br>
                <div style="display: block">
                    <ul style=" list-style-type: none; margin: 0 0 3px 0;">
                        <li>
                            <h2>Planta</h2>
                        </li>
                        <li style="margin: 5 0 5px 0;"><select id="select" onchange="( function(){
                            //Change the value of SelectedFloor and the process of drawing the nodes is performed.
                            selectedFloor = $('#select').val();
                            processNodes(nodes);
                        })();return false;">
                                <option value="0">Planta 0</option>
                                <option value="1">Planta 1</option>
                                <option value="2">Planta 2</option>
                                <option value="-1">Planta S1</option>
                            </select></li>
                        <li>
                            <h2>Tipo de elemento</h2>
                        </li>
                        <li style="margin: 5 0 5px 0;"><label><input type="checkbox" id="People" value=1 checked
                                    onclick="(function() {
                            //Change the value of People from 1 to -1 or from -1 to 1 and perform the process of drawing the nodes.
                            People *= -1;
                            processNodes(nodes);
                        })()">
                                Personas </label> </listyle="margin: 0 0 3px 0;">
                        <li style="margin: 5 0 5px 0;"><label><input type="checkbox" id="Devices" value=1 checked
                                    onclick="(function() {
                            //Change the value of Devices from 1 to -1 or from -1 to 1 and perform the process of drawing the nodes.
                            Devices *= -1;
                            processNodes(nodes);
                        })()">
                                Dispositivos </label></li>
                        <li>
                            <h2>Áreas </h2>
                        </li>
                        <li style="margin: 5 0 5px 0;"><label><input type="checkbox" id="aula" onclick="(function() {
                            //Change the value of Aula from 1 to -1 or from -1 to 1 and perform the process of drawing the nodes.
                            Aula *= -1;
                            processNodes(nodes);
                        })()" checked value=1>
                                Aula </label></li>
                        <li style="margin: 5 0 5px 0;"><label><input type="checkbox" id="lab" onclick="(function() {
                            //Change the value of Lab from 1 to -1 or from -1 to 1 and perform the process of drawing the nodes.
                            Lab *= -1;
                            processNodes(nodes);
                        })()" checked value=1>
                                Laboratorio </label></li>
                        <li style="margin: 5 0 5px 0;"><label><input type="checkbox" id="despacho" onclick="(function() {
                            //Change the value of Despacho from 1 to -1 or from -1 to 1 and perform the process of drawing the nodes.
                            Despacho *= -1;
                            processNodes(nodes);
                        })()" checked value=1>
                                Despacho </label></li>
                        <li style="margin: 5 0 5px 0;"><label><input type="checkbox" id="comun" onclick="(function() {
                            //Change the value of Comun from 1 to -1 or from -1 to 1 and perform the process of drawing the nodes.
                            Comun *= -1;
                            processNodes(nodes);
                        })()" checked value=1>
                                Pasillo/Común </label></li>
                        <li style="margin: 5 0 5px 0;"><label><input type="checkbox" id="cuarto" onclick="(function() {
                            //Change the value of Cuarto from 1 to -1 or from -1 to 1 and perform the process of drawing the nodes.
                            Cuarto *= -1;
                            processNodes(nodes);
                        })()" checked value=1>
                                Cuarto </label></li>
                        <li style="margin: 5 0 5px 0;"><label><input type="checkbox" id="aseo" onclick="(function() {
                            //Change the value of Aseo from 1 to -1 or from -1 to 1 and perform the process of drawing the nodes.
                            Aseo *= -1;
                            processNodes(nodes);
                        })()" checked value=1>
                                Aseo </label></li>
                        <li style="margin: 5 0 5px 0;"><label><input type="checkbox" id="sala" onclick="(function() {
                            //Change the value of Sala from 1 to -1 or from -1 to 1 and perform the process of drawing the nodes.
                            Sala *= -1;
                            processNodes(nodes);
                        })()" checked value=1>
                                Sala </label></li>
                    </ul>
                </div>
            </div>
            <div class="sidebar-pane" id="search">
                <h1 class="sidebar-header">
                    Consultas
                    <span class="sidebar-close"><i class="fa fa-caret-right"></i></span>
                </h1>
                <br>
                <input type="text" placeholder="Search..">
                <button onclick="sendQuery()"> Buscar </button>
            </div>
            <div class="sidebar-pane" id="settings">
                <h1 class="sidebar-header">Settings<span class="sidebar-close"><i class="fa fa-caret-right"></i></span>
                </h1>
            </div>
        </div>
    </div>


    <script>
        //Create the map object and insert the div with id 'mapid'. The initial coordinates 39.47.. and -6.34.. are selected. 
        // and zoom 20.
        var map = L.map('mapid', { zoomDelta: 0.5, zoomSnap: 0.5 }).setView([39.47841096088879, -6.340684443712235], 20);

        //Loading the map display layer.
        var streets = L.tileLayer('https://api.mapbox.com/styles/v1/mapbox/streets-v10/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1IjoiZmFoYW5pIiwiYSI6ImNqMTZiYm4xMjAyYjEzMnFxdmxnd2V3cHkifQ.-8Hau4tMxMiiSF-9D5AAYA', { maxZoom: 25 }).addTo(map);
        //Creation of the map sidebar. is inserted into the div 'sidebar
        var sidebar = L.control.sidebar('sidebar').addTo(map);
        //Array in which the areas that have already been loaded into the display are stored.
        var Areas = []

        //transforms a bounds type object (obtained with map.getBounds()) to a polygon in the turf library.
        let toPoly = (bounds) => turf.polygon([[
            [bounds.getNorthWest().lng, bounds.getNorthWest().lat],
            [bounds.getNorthEast().lng, bounds.getNorthEast().lat],
            [bounds.getSouthEast().lng, bounds.getSouthEast().lat],
            [bounds.getSouthWest().lng, bounds.getSouthWest().lat],
            [bounds.getNorthWest().lng, bounds.getNorthWest().lat]]]);

        //Action executed at the end of a movement on the display.
        map.on('moveend', function onDragEnd(s) {
            console.log(map.getZoom());

            //Get the current visible area.
            var Area_Visible = [toPoly(map.getBounds())];
            //Keeps a copy as it will be changed later.
            let original = Area_Visible[0];
            //Flag to check if the area is new or contained in an already obtained one.
            var is_new_area = true;

            //1. Iterate over all the areas already saved.
            //2. For each one, it checks if the new area is within the upper area.
            //3.a If it is, the loop is broken and the process is not completed.
            //3.b If it is not, the difference between the two areas is made.
            // This returns a polygon object which may be composed of one or more polygons.
            //4. If there are several polygons, they are divided into simple polygons since the operation 
            //BooleanContains and Difference do not support the MultiPolygon type. As the process progresses, 
            // the polygon is cut out until an area is obtained in which there is no information already consulted. 
            isnew: for (var i = 0; i < Areas.length; i++) {
                //This is a loop because from the second iteration we can have more than one polygon
                for (var j = 0; j < Area_Visible.length; j++) {
                    if (turf.booleanContains(Areas[i], Area_Visible[j])) {
                        is_new_area = false;
                        //Break the superior loop.
                        break isnew;
                    } else {
                        val = turf.difference(Area_Visible[j], Areas[i]);
                        //Return null if they are the exact same polygon.
                        Area_Visible[j] = val != null ? val : Area_Visible[j]
                        if (Area_Visible[j].geometry.type == "MultiPolygon") {
                            //Convert MultiPolygon to multiple single polygon.
                            for (x = 1; x < Area_Visible[j].geometry.coordinates.length; x++) {
                                Area_Visible.push(turf.polygon(Area_Visible[j].geometry.coordinates[x]))
                            }
                            Area_Visible[j] = turf.polygon(Area_Visible[j].geometry.coordinates[0])

                        }
                    }
                }
            }
            // If the area is new and the zoom in the viewfinder is adequate, the query is made.
            if (is_new_area && map.getZoom() >= 18) {
                //Only the upper areas are kept, if an area is contained in another it is removed.
                //if an area is contained in another it is removed.
                Areas = Areas.filter(area => !turf.booleanContains(original, area));
                Areas.push(original);
                //Query the database.
                queryNeo4j(Area_Visible.map(e => e.geometry.coordinates[0]))
            }

            //If there are nodes saved, the process of drawing on the map is carried out.
            if (nodes != null) {
                processNodes(nodes);
            }


        });


        /*
        //It doesn't work until we put https in zato
        //Put a marker in the user position
        function onLocationFound(e) {
            var radius = e.accuracy;

            L.marker(e.latlng).addTo(map)
                .bindPopup("You are within " + radius + " meters from this point").openPopup();

            L.circle(e.latlng, radius).addTo(map);
        }

        //callback invoked when the location is found.
        map.on('locationfound', onLocationFound);

        //Get the location every 5 seconds
        locate = () => map.locate({setView: true, maxZoom: 16});
        setInterval(locate, 5000);
        */

        //Arrays with geoJson data and nodes Ids. They are used to draw the polygons in the viewer.
        var layers = [];
        var layersIds = [];

        //Array with the Neo4j nodes, this variable is actualized every time queryNeo4j is called.
        var nodes = [];


        //Checkbox and floor variables initialization
        var selectedFloor = parseInt($('#select').val());
        var People = $('#People:checked').val() == "1" ? 1 : -1;;
        var Devices = $('#Devices:checked').val() == "1" ? 1 : -1;;
        var Aseo = $('#aseo:checked').val() == "1" ? 1 : -1;
        var Aula = $('#aula:checked').val() == "1" ? 1 : -1;
        var Lab = $('#lab:checked').val() == "1" ? 1 : -1;
        var Comun = $('#comun:checked').val() == "1" ? 1 : -1;
        var Despacho = $('#despacho:checked').val() == "1" ? 1 : -1;
        var Sala = $('#sala:checked').val() == "1" ? 1 : -1;
        var Cuarto = $('#cuarto:checked').val() == "1" ? 1 : -1;

        //First query to the database.
        queryNeo4j(toPoly(map.getBounds()).geometry.coordinates);

        defineDiff();

        function processNodes(nodes) {

            // Collect the ids of the building nodes that matches the spatial query.
            let nodesToDraw = [];
            let matchedNodes = []
            //Get the nodes we are going to Draw
            matchingNodes(nodes, matchedNodes, nodesToDraw);


            //Get the difference between matching nodes and and those already drawn and remove it.
            let nodesToRemove = layersIds.diff(matchedNodes);
            removeNodes(nodesToRemove);

            //For each node mathed.
            matchedNodes.forEach(function (nodeToAdd) {

                // add it if the node doesn't exist in the map
                if (!layers[nodeToAdd]) {

                    // add it if the node has the geojson property and the geojson is valid json
                    if (nodesToDraw[nodeToAdd].geojson != undefined && isJson(nodesToDraw[nodeToAdd].geojson)) {
                        //Save the node id. This is used later to remove the previouly drawn nodes. 
                        layersIds.push(nodeToAdd);

                        //If the node is of the alert type, another type of operation must be performed.
                        if (nodesToDraw[nodeToAdd].Alerts) {
                            //Calling the service that checks if the alert needs to be activated.
                            fetch(nodesToDraw[nodeToAdd].Alerts).then(function (response) {
                                return response.json();
                            }).then(response => {
                                let json = response;
                                //Check the alert query result
                                if (json == "aviso") {
                                    drawNode(layers, nodesToDraw, nodeToAdd);
                                }
                            });

                        } else {
                            drawNode(layers, nodesToDraw, nodeToAdd);
                        }
                    }
                }
            });

        }

        //The function iterates the list of nodes and selects those to be drawn.  
        //This is done by checking the zoom of the viewer, the selected filters and the selected floor.
        function matchingNodes(nodes, matchedNodes, nodesToDraw) {

            nodes.forEach(function (node) {

                //Filter by floor and checkbox values
                if (Devices == -1 && node.graph.nodes[0].labels[0] == "Device") { return; }
                if (People == -1 && node.graph.nodes[0].labels[0] == "People") { return; }
                if (node.graph.nodes[0].labels[0] == "Room" && Aseo == -1 && node.graph.nodes[0].properties.type.toLowerCase() == "aseo") { return; }
                if (node.graph.nodes[0].labels[0] == "Room" && Aula == -1 && node.graph.nodes[0].properties.type.toLowerCase() == "aula") { return; }
                if (node.graph.nodes[0].labels[0] == "Room" && Lab == -1 && node.graph.nodes[0].properties.type.toLowerCase() == "laboratorio") { return; }
                if (node.graph.nodes[0].labels[0] == "Room" && Comun == -1 && node.graph.nodes[0].properties.type.toLowerCase() == "comun") { return; }
                if (node.graph.nodes[0].labels[0] == "Room" && Despacho == -1 && node.graph.nodes[0].properties.type.toLowerCase() == "despacho") { return; }
                if (node.graph.nodes[0].labels[0] == "Room" && Sala == -1 && node.graph.nodes[0].properties.type.toLowerCase() == "sala") { return; }
                if (node.graph.nodes[0].labels[0] == "Room" && Cuarto == -1 && node.graph.nodes[0].properties.type.toLowerCase() == "cuarto") { return; }
                if (node.graph.nodes[0].properties.id == undefined) { return; }


                // Check if node is between their properties min_zoom and max_zoom.
                if (node.graph.nodes[0].properties.min_zoom <= map.getZoom() && map.getZoom() <= node.graph.nodes[0].properties.max_zoom || map.getZoom() > 50) {

                    // If it is a floor, add only the selected ones
                    if (node.graph.nodes[0].labels[0] == "Floor") {
                        if (node.graph.nodes[0].properties.id == "UEXCC_TEL_P0" + selectedFloor || node.graph.nodes[0].properties.id == "UEXCC_INF_P0" + selectedFloor || node.graph.nodes[0].properties.id == "UEXCC_ATE_P0" + selectedFloor || node.graph.nodes[0].properties.id == "UEXCC_OPU_P0" + selectedFloor || node.graph.nodes[0].properties.id == "UEXCC_INV_P0" + selectedFloor || node.graph.nodes[0].properties.id == "UEXCC_INV_PS" + (parseInt(selectedFloor) + 2) || node.graph.nodes[0].properties.id == "UEXCC_TEL_PS" + (parseInt(selectedFloor) + 2) || node.graph.nodes[0].properties.id == "UEXCC_SCO_P0" + selectedFloor) {
                            matchedNodes.push(node.graph.nodes[0].properties.id);
                            nodesToDraw[node.graph.nodes[0].properties.id] = node.graph.nodes[0].properties;
                        }
                        // Always add Buildings.
                    } else if (node.graph.nodes[0].labels[0] == "Building") {
                        matchedNodes.push(node.graph.nodes[0].properties.id);
                        nodesToDraw[node.graph.nodes[0].properties.id] = node.graph.nodes[0].properties;
                    } /*else if (node.graph.nodes[0].labels[0] == "Provincia")
                    {
                        matchedNodes.push(node.graph.nodes[0].properties.id);
                        nodesToDraw[node.graph.nodes[0].properties.id] = node.graph.nodes[0].properties;
                    }
                    else if (node.graph.nodes[0].labels[0] == "Pueblo")
                    {
                        matchedNodes.push(node.graph.nodes[0].properties.id);
                        nodesToDraw[node.graph.nodes[0].properties.id] = node.graph.nodes[0].properties;
                    }*/
                    else if (node.graph.nodes[0].labels[0] == "Parcela")
                    {
                        matchedNodes.push(node.graph.nodes[0].properties.id);
                        nodesToDraw[node.graph.nodes[0].properties.id] = node.graph.nodes[0].properties;
                    }
                    // Always add Alerts.
                    else if (node.graph.nodes[0].labels[0] == "Alerts") {
                        matchedNodes.push(node.graph.nodes[0].properties.id);
                        nodesToDraw[node.graph.nodes[0].properties.id] = node.graph.nodes[0].properties;

                    } else if (selectedFloor == 0) {
                        //We use the name attribute to identify which floor is each node on.
                        if (node.graph.nodes[0].properties.id.substr(0, 13) == "UEXCC_TEL_P0" + selectedFloor || node.graph.nodes[0].properties.id.substr(0, 13) == "UEXCC_INF_P0" + selectedFloor || node.graph.nodes[0].properties.id.substr(0, 13) == "UEXCC_ATE_P0" + selectedFloor || node.graph.nodes[0].properties.id.substr(0, 13) == "UEXCC_OPU_P0" + selectedFloor || node.graph.nodes[0].properties.id.substr(0, 13) == "UEXCC_INV_P0" + selectedFloor || node.graph.nodes[0].properties.id.substr(0, 13) == "UEXCC_INV_PS" + (parseInt(selectedFloor) + 2) || node.graph.nodes[0].properties.id.substr(0, 13) == "UEXCC_TEL_PS" + (parseInt(selectedFloor) + 2) || node.graph.nodes[0].properties.id.substr(0, 13) == "UEXCC_SCO_P0" + selectedFloor) {
                            matchedNodes.push(node.graph.nodes[0].properties.id);
                            nodesToDraw[node.graph.nodes[0].properties.id] = node.graph.nodes[0].properties;
                        }
                    } else if (selectedFloor == 1) {
                        //We use the name attribute to identify which floor is each node on.
                        if (node.graph.nodes[0].properties.id.substr(0, 13) == "UEXCC_TEL_P0" + selectedFloor || node.graph.nodes[0].properties.id.substr(0, 13) == "UEXCC_INF_P0" + selectedFloor || node.graph.nodes[0].properties.id.substr(0, 13) == "UEXCC_ATE_P0" + selectedFloor || node.graph.nodes[0].properties.id.substr(0, 13) == "UEXCC_OPU_P0" + selectedFloor || node.graph.nodes[0].properties.id.substr(0, 13) == "UEXCC_INV_P0" + selectedFloor || node.graph.nodes[0].properties.id.substr(0, 13) == "UEXCC_INV_PS" + (parseInt(selectedFloor) + 2) || node.graph.nodes[0].properties.id.substr(0, 13) == "UEXCC_TEL_PS" + (parseInt(selectedFloor) + 2) || node.graph.nodes[0].properties.id.substr(0, 13) == "UEXCC_SCO_P0" + selectedFloor) {
                            matchedNodes.push(node.graph.nodes[0].properties.id);
                            nodesToDraw[node.graph.nodes[0].properties.id] = node.graph.nodes[0].properties;
                        }
                    } else if (selectedFloor == 2) {
                        //We use the name attribute to identify which floor is each node on.
                        if (node.graph.nodes[0].properties.id.substr(0, 13) == "UEXCC_TEL_P0" + selectedFloor || node.graph.nodes[0].properties.id.substr(0, 13) == "UEXCC_INF_P0" + selectedFloor || node.graph.nodes[0].properties.id.substr(0, 13) == "UEXCC_ATE_P0" + selectedFloor || node.graph.nodes[0].properties.id.substr(0, 13) == "UEXCC_OPU_P0" + selectedFloor || node.graph.nodes[0].properties.id.substr(0, 13) == "UEXCC_INV_P0" + selectedFloor || node.graph.nodes[0].properties.id.substr(0, 13) == "UEXCC_INV_PS" + (parseInt(selectedFloor) + 2) || node.graph.nodes[0].properties.id.substr(0, 13) == "UEXCC_TEL_PS" + (parseInt(selectedFloor) + 2) || node.graph.nodes[0].properties.id.substr(0, 13) == "UEXCC_SCO_P0" + selectedFloor) {
                            matchedNodes.push(node.graph.nodes[0].properties.id);
                            nodesToDraw[node.graph.nodes[0].properties.id] = node.graph.nodes[0].properties;
                        }
                    } else if (selectedFloor == -1) {
                        //We use the name attribute to identify which floor is each node on.
                        if (node.graph.nodes[0].properties.id.substr(0, 13) == "UEXCC_TEL_P0" + selectedFloor || node.graph.nodes[0].properties.id.substr(0, 13) == "UEXCC_INF_P0" + selectedFloor || node.graph.nodes[0].properties.id.substr(0, 13) == "UEXCC_ATE_P0" + selectedFloor || node.graph.nodes[0].properties.id.substr(0, 13) == "UEXCC_OPU_P0" + selectedFloor || node.graph.nodes[0].properties.id.substr(0, 13) == "UEXCC_INV_P0" + selectedFloor || node.graph.nodes[0].properties.id.substr(0, 13) == "UEXCC_INV_PS" + (parseInt(selectedFloor) + 2) || node.graph.nodes[0].properties.id.substr(0, 13) == "UEXCC_TEL_PS" + (parseInt(selectedFloor) + 2) || node.graph.nodes[0].properties.id.substr(0, 13) == "UEXCC_SCO_P0" + selectedFloor) {
                            matchedNodes.push(node.graph.nodes[0].properties.id);
                            nodesToDraw[node.graph.nodes[0].properties.id] = node.graph.nodes[0].properties;
                        }
                    }
                }
            });
        }

        //Draw a node on the map
        function drawNode(layers, nodesToDraw, nodeToAdd) {
            //Obtain the geoJSON and create the marker to be seen in the viewer. 
            //For this, we use the property image of the node.
            layers[nodeToAdd] = L.geoJSON(JSON.parse(nodesToDraw[nodeToAdd].geojson),
                {
                    pointToLayer:
                        //Creates a marker with the image of the node at the node position (latitude, longitude)   
                        function (feature, latlng) {
                            if (nodesToDraw[nodeToAdd].img) {
                                let icon = L.icon({ iconUrl: nodesToDraw[nodeToAdd].img });
                                return L.marker(latlng, { icon: icon });
                            } else if (nodesToDraw[nodeToAdd].Alertsimg) {
                                let icon = L.icon({ iconUrl: nodesToDraw[nodeToAdd].Alertsimg });
                                return marker = L.marker(latlng, { icon: icon })
                            }
                        },
                    style:
                        //Returns the style that will be used to draw the node.
                        //This value is found in the geoJSON.
                        function (feature) {
                            return {
                                color: feature.style.fill ? feature.style.fill : '#3388ff',
                                fillOpacity: feature.style.fill_opacity ? feature.style.fill_opacity : 0.4,
                                width: 2

                            };
                        },
                    onEachFeature:
                        //A label is added with the node information. 
                        //It can contain a pdf, a link to grafana , etc.
                        function onEachFeature(feature, layer) {

                            let bindText = "";
                            //If the node has a data source, it adds it 
                            if (nodesToDraw[nodeToAdd].dataSource) {
                                bindText = bindText + "" + nodesToDraw[nodeToAdd].dataSource + "<br> <a href='" + $(nodesToDraw[nodeToAdd].dataSource)[0].src + "' target='_blank'>Abrir en ventana</a>";
                            }
                            //If it does not, it adds its name and identifier.
                            else if (feature.properties && feature.properties.name)
                                bindText = bindText + "" + nodesToDraw[nodeToAdd].name + "<br> " + nodesToDraw[nodeToAdd].id;
                            
                            else if (feature.properties)
                                Object.keys(feature.properties).forEach(key => bindText +=  "<span> <b>" + key + "</b> : " + feature.properties[key] +  "</span> <br> ")
                            //If it has neither, it leaves it empty.
                            else
                                bindText = ""

                            //Creates a popup that opens when you click on the marker.
                            var p = layer.bindPopup(bindText, {
                                minWidth: "auto",
                                maxWidth: "auto",
                                maxHeight: "auto"
                            });

                        }
                });
            //Add node to map.
            layers[nodeToAdd].addTo(map);
        }



        //Removen nodes from the map.
        function removeNodes(nodesToRemove) {
            nodesToRemove.forEach(function (nodeToRemove) {
                if (layers[nodeToRemove]) {
                    map.removeLayer(layers[nodeToRemove]);
                }
                delete layers[nodeToRemove];

                let index = layersIds.indexOf(nodeToRemove);
                if (index > -1) {
                    layersIds.splice(index, 1);
                }
            });

        }

        //Make a query to the Neo4j service. 
        //The polygon or polygons of the request will be sent as a parameter.
        function queryNeo4j(val) {

            $.ajax({
                url: "http://158.49.112.127:11223/neozip",
                headers: {
                    "Cache-Control": "public",
                },
                type: "POST",
                data: JSON.stringify({
                    "query": val
                }),
                error: function (err) {
                    alert("error");
                },
                success: function (res) {
                    //The answer to the request is compressed in zip format to reduce its size. 
                    //(If this is done, the answers can take up to tens of megabytes.)
                    res = atob(res)
                    var data = new Array(res.length);
                    for (i = 0, il = res.length; i < il; ++i) {
                        data[i] = res.charCodeAt(i);
                    }

                    var inflate = new Zlib.Inflate(data);
                    var decompress = inflate.decompress();
                    res = JSON.parse(new TextDecoder("utf-8").decode(decompress))
                    //If response is Ok.
                    if (res.results) {
                        new_nodes = res.results[0].data;
                        //Add nodes that are new.
                        new_nodes.forEach(node => {
                            not_found = true;
                            for (var i = 0; i < nodes.length; i++) {
                                if (nodes[i].graph.nodes[0].properties.id == node.graph.nodes[0].properties.id) {
                                    not_found = false;
                                    return;
                                }
                            }
                            nodes.push(node);
                        });

                        console.log(nodes);
                        processNodes(nodes);
                    }
                }
            });
        }

        //check if object can be parsed to json.
        function isJson(item) {
            item = typeof item !== "string"
                ? JSON.stringify(item)
                : item;

            try {
                item = JSON.parse(item);
            } catch (e) {
                return false;
            }

            if (typeof item === "object" && item !== null) {
                return true;
            }

            return false;
        }

        // Define diff function in arrays
        function defineDiff() {
            Array.prototype.diff = function (a) {
                return this.filter(function (i) {
                    return a.indexOf(i) === -1;
                });
            };
        }

    </script>

</body>

</html>
  
        """

        self.response.content_type = 'text/html; charset=utf-8'
