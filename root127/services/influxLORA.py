#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from zato.server.service import Service
from influxdb import InfluxDBClient
import json


class PruebaInfluxZato(Service):

    def connectToDb(self):
        client = InfluxDBClient(host='158.49.247.206', port=8086)
        client.switch_database('pruebalora')
        return client

    def comprobartabla(self, entrada, client):
        existe=False
        for r in client.get_list_measurements():
            if r['name'] == entrada['dev_id']:
                existe=True

        return existe

    def handle(self):

        try:
            self.logger.info(type(self.request.payload))
            self.logger.info(self.request.payload)
            self.logger.info(self.request.payload['payload_fields'])
            entrada= self.request.payload
            client= self.connectToDb()
            json_body = []
            informacion={
                'measurement': entrada['dev_id'],
                'tags': {'apikey': entrada['app_id']},
                'fields': entrada['payload_fields']
            }
            json_body.append(informacion)
            datoinside = client.write_points(json_body)
            if datoinside:
                self.response.payload = "Dato Insertado Correctamente"
            else:
                self.response.payload = "Fallo en la estructura del JSON"
        except ValueError:
            self.response.payload = "No se ha podido parsear el json o ha habido un problema de conexión"
