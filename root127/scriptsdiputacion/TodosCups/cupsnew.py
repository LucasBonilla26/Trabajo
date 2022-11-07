import glob
import requests
import json
from bs4 import BeautifulSoup
from influxdb import InfluxDBClient
import json
import time
import datetime
import calendar




def connectToDb(self):
    client = InfluxDBClient(host='158.49.112.127', port=8086)
    client.switch_database('CUPS_CASAR')
    return client


client = InfluxDBClient(host='158.49.112.127', port=8086)
client.switch_database('CUPS_CASAR')
token=open ('/root/scriptsdiputacion/TodosCups/token.txt','r')
token=token.read()
hed = {'Authorization': 'Bearer ' + str(token)}




comprobacion=requests.get("https://datadis.es/api-private/api/get-consumption-data?cups=ES0102050220331801FS0F&distributorCode=6&startDate=2018%2F01%2F01&endDate=2018%2F01%2F02&measurementType=0&pointType=5", verify=False, stream=True, headers=hed)
if str(comprobacion) == '<Response [401]>':
    tokenquery = 'https://datadis.es/nikola-auth/tokens/login?username=P1005000C&password=Casar*2021'
    hed = requests.post(tokenquery, verify=False, stream=True)
    f = open('/root/scriptsdiputacion/TodosCups/token.txt', 'wt')
    f.write(hed.text)
    hed = {'Authorization': 'Bearer ' + str(hed.text)}



cups= requests.get('https://datadis.es/api-private/api/get-supplies', verify=False, stream=True, headers=hed)



f = open ('/root/scriptsdiputacion/TodosCups/cups_ayto','r')
listado = f.read()
separado = listado.split("\n")
f.close()
newdata=[]
with open('/root/scriptsdiputacion/TodosCups/listadocups.json') as file:
    data = json.load(file)
for i in data:
    if i['cups'] in separado:
        newdata.append(i)
data = newdata



#year='0001'
#print('year')
#month='12'
#day='15'
#yearend = '2022'
#monthend = '01'
#dayend = '30'



now=(datetime.datetime.now())
day="01"
if now.month != 1 :
    year = str(now.year)
    if now.month-1 < 10:
        month = "0" + str(now.month - 1)
    else:
        month = str(now.month - 1)

    monthend = month
    dayend = str(calendar.monthrange(now.year, now.month-1)[1])

else:
    year = str(now.year-1)
    month = "12"
    monthend = month
    dayend = str(calendar.monthrange(now.year, 12)[1])

print(year, month, day, dayend, monthend)
yearend=year
#day = "01"
#month = "02"
#monthend = "04"
#dayend = "01"
#year = "2022"
#yearend = "2022"
#print(year, yearend)

for r in data:
    query = "https://datadis.es/api-private/api/get-consumption-data?cups={cups}&distributorCode={distributorCode}&startDate={year}%2F{month}%2F{day}&endDate={yearend}%2F{monthend}%2F{dayend}&measurementType=0&pointType={pointType}".format(
        cups = r['cups'], distributorCode=r['distributorCode'], pointType=r['pointType'], year=year, month=month, day=day, yearend=yearend, monthend=monthend, dayend=dayend)
    print(query)
    cup = requests.get(query, verify=False, stream=True, headers=hed)
    jsondata = cup.json()
    jsondata = jsondata

    for x in jsondata:
        fecha = x['date']
        hora = x['time']
        if hora[0:2]=='24':
            hora='00'
        fecha = fecha + '/' + hora[0:2]
        tiempo = time.mktime(datetime.datetime.strptime(fecha, "%Y/%m/%d/%H").timetuple())
        tiempo = int(tiempo)
        consumoKWh = x['consumptionKWh']
        metodo=x['obtainMethod']
        json_body = []
        informacion = {'measurement': r['cups'], 'tags': {'Direccion': r['address'], 'MetodoObtencion': metodo},
                       'fields': {'Consumo': consumoKWh}, 'time': tiempo}
        json_body.append(informacion)
        datoinside = client.write_points(json_body, time_precision='s')
