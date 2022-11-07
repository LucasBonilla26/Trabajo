#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from zato.server.service import Service
from influxdb import InfluxDBClient
import json


class PruebaInfluxZato(Service):

    class SimpleIO:
        input_required = ("json",)
        #output_required

    def connectToDb(self):
        client = InfluxDBClient(host='158.49.112.127', port=8086)
        client.switch_database('sensors')
        return client



    def handle(self):

        try:
            client= self.connectToDb()
            entrada = json.loads(self.request.input.json)
            json_body = []
            informacion={
                'measurement': entrada['info']['device'],
                'tags': {'apikey': entrada['info']['api_key']},
                'fields': entrada['data']
            }
            json_body.append(informacion)
            datoinside = client.write_points(json_body)
            if datoinside:
                self.response.payload = "Dato Insertado Correctamente"
            else:
                self.response.payload = "Fallo en la estructura del JSON"
        except ValueError:
            self.response.payload = "No se ha podido parsear el json o ha habido un problema de conexión"
