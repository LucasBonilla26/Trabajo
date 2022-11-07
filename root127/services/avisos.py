from zato.server.service import Service
import requests
from influxdb import InfluxDBClient
import json
import datetime
class avisos(Service):

    def influxCall(self):
        client = InfluxDBClient(host='10.253.247.18', port=8086, username='r0b0l4b', password='alwayssmarter4')
        client.switch_database('sensors')

        ValoresEstimados_a = {"00": 2, "01": 2, "02": 4, "03": 3, "04": 4, "05": 28, "06": 53, "07": 65, "08": 86,
                              "09": 123, "10": 131, "11": 120, "12": 107, "13": 129, "14": 123, "15": 95,
                              "16": 74, "17": 44, "18": 39, "19": 16, "20": 5, "21": 4, "22": 3, "23": 3}

        nameofsensor_a = "UEXCC_INF_P00_CUA002_SEN002_AGU"
        consumolasthour_a = 0

        contador = "counter2"
        now = datetime.datetime.now()
        horaActual = now.replace(hour=now.hour, minute=00)
        horaSiguiente = now.replace(hour=horaActual.hour + 1, minute=00)
        query = "Select %s from %s WHERE time >= '%s' and time < '%s'" % (
            contador, nameofsensor_a, horaActual, horaSiguiente)
        lastvalue_a = list(client.query(query))

        for a in lastvalue_a:
            for b in a:
                consumolasthour_a += b['counter2']
        print(consumolasthour_a)
        if horaActual.hour < 10:
            if consumolasthour_a * 10 > ValoresEstimados_a["0" + str(horaActual.hour)]:
                aviso="aviso"
            else:
                aviso="nada"
        else:
            if consumolasthour_a * 10 > ValoresEstimados_a[str(horaActual.hour)]:
                aviso="aviso"
            else:
                aviso="nada"
        return aviso

    def handle(self):
        self.response.payload = json.dumps(self.influxCall())
