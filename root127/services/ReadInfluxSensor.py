# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from zato.server.service import Service #Necesario para que funcione en Zato
from influxdb import InfluxDBClient
import json
import re

class ReadInfluxSensor(Service):

    class SimpleIO: #Clase SimpleIO explicada en la documentación de Zato
        input_required = ("json",) #Input por navegador necesario en formato JSON
        #output_required

    def connectToDb(self): #Conectamos  influxDB
        client = InfluxDBClient(host='10.253.247.18', port=8086, username='r0b0l4b', password='alwayssmarter4') # Conectamos a la base de datos Influx de SmartPOliTech introduciendo puerto y usuario-contraseña
        client.switch_database('sensors')# seleccionamos la base de datos sensors donde se encuentran los datos de los sensores
        return client

    def comprobartabla(self, entrada, client):#comprobación de si existe el sensor que se desea consultar
        existe = False
        for r in client.get_list_measurements():#obtenemos la lista de sensores que están almacenados en la base de datos sensors
            if r['name'] == entrada['info']['device']: #comprobación de que el sensor introducido existe
                existe = True#si existe devolvemos true

        return existe

    def validDateRange(self, input):#validación del rango de fechas introducido con expresión regular

        p = re.compile(
            '^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\\.[0-9]+)?(Z)?$')

        if 'from' in input["info"] and not p.match(input["info"]["from"]):
            return False
        if 'to' in input["info"] and not p.match(input["info"]["to"]):
            return False

        return True

    def queryToDevices(self, input, client):
        sensor=input['info']['device']
        fromDate = None
        toDate = None

        json_body = []
        if 'from' in input["info"]:
            fromDate = input["info"]["from"]

        if 'to' in input["info"]:
            toDate = input["info"]["to"]

        if fromDate is not None and toDate is not None:
            fromDate=fromDate.split("T")[0]+ " "+ fromDate.split("T")[1]
            toDate=toDate.split("T")[0]+ " "+ toDate.split("T")[1]
            query = "Select * from %s where time >= '%s' and time < '%s' GROUP BY * LIMIT 1500" % (sensor, fromDate, toDate)
            results = client.query(query)
            #points = results.get_points(tags={'apikey': '000000'})
            li = list(results.get_points())
            KeyDatos = results.raw['series'][0]['columns']
            long = len(KeyDatos)
            for punto in li:
                dicc = {}
                if 'ip' in punto:
                    if punto['ip'] == None:
                        for key in KeyDatos[1:long - 1]:
                            dicc[key] = punto[key]
                            # print(key)
                            # print(dicc)
                    else:
                        for key in KeyDatos[1:]:
                            dicc[key] = punto[key]
                else:
                    for key in KeyDatos[1:]:
                        dicc[key] = punto[key]
                json_inter = {
                    'created_at': punto['time'],
                    'data': dicc
                }
                json_body.append(json_inter)
        else:
            query = "Select * from %s  ORDER BY time DESC LIMIT 1500" % (sensor)
            results = client.query(query)
            # points = results.get_points(tags={'apikey': '000000'})
            li = list(results.get_points())
            KeyDatos = results.raw['series'][0]['columns']
            long = len(KeyDatos)
            for punto in li:
                dicc = {}
                if 'ip' in punto:
                    if punto['ip'] == None:
                        for key in KeyDatos[1:long - 1]:
                            dicc[key] = punto[key]
                            # print(key)
                            # print(dicc)
                    else:
                        for key in KeyDatos[1:]:
                            dicc[key] = punto[key]
                else:
                    for key in KeyDatos[1:]:
                        dicc[key] = punto[key]
                json_inter = {
                    'created_at': punto['time'],
                    'data': dicc
                }
                json_body.append(json_inter)

        return json.dumps(json_body)

    def handle(self):
        try:
            input = json.loads(self.request.input.json)
            client = self.connectToDb()
            self.connectToDb()

            if 'info' not in input:
                self.response.payload = {"error": "Invalid JSON structure"}
            elif 'device' not in input["info"]:
                self.response.payload = {"error": "Invalid JSON structure. Missing device table"}
            elif 'api_key' not in input["info"]:
                self.response.payload = {"error": "Invalid JSON structure. Missing api_key"}
            elif self.comprobartabla(input,client) == False:
                self.response.payload = {"error": "Invalid device table"}
            elif self.validDateRange(input) == False:
                self.response.payload = {"error": "Invalid date format. It should be in iso8601. Example: 2018-02-07T12:00:52"}
            else:
                self.response.payload = self.queryToDevices(input, client)


        except ValueError:
            self.response.payload = "No se ha podido parsear el json"

        # except:
        #    self.response.payload = "Excepcion generica"
