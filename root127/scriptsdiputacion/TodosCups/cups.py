import glob
import requests
import json
from bs4 import BeautifulSoup
from influxdb import InfluxDBClient
import json
import time
import datetime


def connectToDb(self):
    client = InfluxDBClient(host='158.49.112.127', port=8086)
    client.switch_database('CUPS_CASAR')
    return client


client = InfluxDBClient(host='158.49.112.127', port=8086)
client.switch_database('CUPS_CASAR')
token=open ('token.txt','r')
token=token.read()
hed = {'Authorization': 'Bearer ' + str(token)}




comprobacion=requests.get("https://datadis.es/api-private/api/get-consumption-data?cups=ES0102050220331801FS0F&distributorCode=6&startDate=2018%2F01%2F01&endDate=2018%2F01%2F02&measurementType=0&pointType=5", verify=False, stream=True, headers=hed)
if str(comprobacion)=='<Response [401]>':
    tokenquery = 'https://datadis.es/nikola-auth/tokens/login?username=P1005000C&password=Casar*2021'
    hed = requests.post(tokenquery, verify=False, stream=True)
    f = open('token.txt', 'wt')
    f.write(hed.text)
    hed = {'Authorization': 'Bearer ' + str(hed.text)}



cups= requests.get('https://datadis.es/api-private/api/get-supplies', verify=False, stream=True, headers=hed)
print(cups)


f = open ('cups_ayto','r')
listado=f.read()
separado=listado.split("\n")
print(len(separado))
f.close()
newdata=[]
with open('listadocups.json') as file:
    data = json.load(file)
for i in data:
    if i['cups'] in separado:
        newdata.append(i)
data=newdata


year='2018'
month='01'
day='01'
yearend='2021'
monthend='01'
dayend='01'

for r in data:
    year = '2018'
    month = '01'
    day = '01'
    try:
        yearend = '2020'
        query = "https://datadis.es/api-private/api/get-consumption-data?cups={cups}&distributorCode={distributorCode}&startDate={year}%2F{month}%2F{day}&endDate={yearend}%2F{monthend}%2F{dayend}&measurementType=0&pointType={pointType}".format(
            cups=r['cups'], distributorCode=r['distributorCode'], pointType=r['pointType'], year=year, month=month, day=day, yearend=yearend, monthend=monthend, dayend=dayend)
        query_seg = "https://datadis.es/api-private/api/get-consumption-data?cups={cups}&distributorCode={distributorCode}&startDate=2020%2F{month}%2F{day}&endDate=2021%2F03%2F01&measurementType=0&pointType={pointType}".format(
            cups=r['cups'], distributorCode=r['distributorCode'], pointType=r['pointType'], year=year, month=month,
            day=day, yearend=yearend, monthend=monthend, dayend=dayend)
        cup = requests.get(query, verify=False, stream=True, headers=hed)
        cup_dos = requests.get(query_seg, verify=False, stream=True, headers=hed)
        jsondata = cup.json()
        jsondata2 = cup_dos.json()
        jsondata = jsondata + jsondata2
    except:
        try:
            year = '2019'
            month = '01'
            day = '01'
            yearend='2021'
            query = "https://datadis.es/api-private/api/get-consumption-data?cups={cups}&distributorCode={distributorCode}&startDate={year}%2F{month}%2F{day}&endDate={yearend}%2F{monthend}%2F{dayend}&measurementType=0&pointType={pointType}".format(
                cups=r['cups'], distributorCode=r['distributorCode'], pointType=r['pointType'], year=year, month=month,
                day=day, yearend=yearend, monthend=monthend, dayend=dayend)
            query_seg = "https://datadis.es/api-private/api/get-consumption-data?cups={cups}&distributorCode={distributorCode}&startDate=2021%2F{month}%2F{day}&endDate=2021%2F03%2F01&measurementType=0&pointType={pointType}".format(
                cups=r['cups'], distributorCode=r['distributorCode'], pointType=r['pointType'], year=year, month=month,
                day=day, yearend=yearend, monthend=monthend, dayend=dayend)
            cup = requests.get(query, verify=False, stream=True, headers=hed)
            cup_dos=requests.get(query_seg, verify=False, stream=True, headers=hed)
            jsondata = cup.json()
            jsondata2=cup_dos.json()
            jsondata= jsondata+jsondata2
        except:
            year = '2020'
            month = '01'
            day = '01'
            yearend='2021'
            query = "https://datadis.es/api-private/api/get-consumption-data?cups={cups}&distributorCode={distributorCode}&startDate={year}%2F{month}%2F{day}&endDate={yearend}%2F{monthend}%2F{dayend}&measurementType=0&pointType={pointType}".format(
                cups=r['cups'], distributorCode=r['distributorCode'], pointType=r['pointType'], year=year, month=month,
                day=day, yearend=yearend, monthend=monthend, dayend=dayend)
            cup = requests.get(query, verify=False, stream=True, headers=hed)
            jsondata = cup.json()
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
        #datoinside = client.write_points(json_body, time_precision='s')




