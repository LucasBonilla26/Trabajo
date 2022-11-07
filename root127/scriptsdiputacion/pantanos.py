import glob
import requests
import json
from bs4 import BeautifulSoup
from influxdb import InfluxDBClient
import json
import time
import datetime


now=(datetime.datetime.now())
hoy=(now).strftime("%Y-%m-%d")
ayer=(now-datetime.timedelta(days=1)).strftime("%Y-%m-%d")
print(hoy)
print(ayer)
#Conexion Influxdb
client = InfluxDBClient(host='158.49.112.127', port=8086)
client.switch_database('AHIGAL')

fecha_ini=ayer
fecha_fin=hoy


#Extracciondatos
m = requests.get('https://saihtajo.chtajo.es/libs/sedh_lite/ajax.php?url=/sedh/ajax_obtener_tabla_numericos/param:1615285927056/origen:1d/fecha_ini:{fecha_ini}-00-00/fecha_fin:{fecha_fin}-00-00/zoom_ini:{fecha_ini}-00-00/zoom_fin:{fecha_fin}-00-00/_senal:E_36VICT01/_valor:ULT/ver_detalle:1/alto:633&_=1615285927057'.format(fecha_ini=fecha_ini, fecha_fin=fecha_fin), verify=False, stream=True)
cota=requests.get('https://saihtajo.chtajo.es/libs/sedh_lite/ajax.php?url=/sedh/ajax_obtener_tabla_numericos/param:1616579503618/origen:1d/fecha_ini:{fecha_ini}-00-00/fecha_fin:{fecha_fin}-00-00/zoom_ini:{fecha_ini}-00-00/zoom_fin:{fecha_fin}-00-00/_senal:E_36LICT01|E_36LICT01|E_36LICT01/_valor:MED|MAX|MIN/ver_detalle:1/alto:946&_=1616579503619'.format(fecha_ini=fecha_ini, fecha_fin=fecha_fin), verify=False, stream=True)
DireccionViento=requests.get('https://saihtajo.chtajo.es/libs/sedh_lite/ajax.php?url=/sedh/ajax_obtener_tabla_numericos/param:1616581044934/origen:1d/fecha_ini:{fecha_ini}-00-00/fecha_fin:{fecha_fin}-00-00/zoom_ini:{fecha_ini}-00-00/zoom_fin:{fecha_fin}-00-00/_senal:E_36UI__12|E_36UI__12|E_36UI__12/_valor:MED|MAX|MIN/ver_detalle:1/alto:946&_=1616581044934'.format(fecha_ini=fecha_ini, fecha_fin=fecha_fin), verify=False, stream=True)
Humedad=requests.get('https://saihtajo.chtajo.es/libs/sedh_lite/ajax.php?url=/sedh/ajax_obtener_tabla_numericos/param:1616581498886/origen:1d/fecha_ini:{fecha_ini}-00-00/fecha_fin:{fecha_fin}-00-00/zoom_ini:{fecha_ini}-00-00/zoom_fin:2{fecha_fin}-00-00/_senal:E_36UI__14|E_36UI__14|E_36UI__14/_valor:MED|MAX|MIN/ver_detalle:1/alto:946&_=1616581498887'.format(fecha_ini=fecha_ini, fecha_fin=fecha_fin), verify=False, stream=True)
Pluviometro=requests.get('https://saihtajo.chtajo.es/libs/sedh_lite/ajax.php?url=/sedh/ajax_obtener_tabla_numericos/param:1616584258151/origen:1d/fecha_ini:{fecha_ini}-00-00/fecha_fin:{fecha_fin}-00-00/zoom_ini:{fecha_ini}-00-00/zoom_fin:{fecha_fin}-00-00/_senal:E_36WI__01|E_36WI__01|E_36WI__01/_valor:INT|MAX|MED/ver_detalle:1/alto:753&_=1616584258151'.format(fecha_ini=fecha_ini, fecha_fin=fecha_fin), verify=False, stream=True)
Presion=requests.get('https://saihtajo.chtajo.es/libs/sedh_lite/ajax.php?url=/sedh/ajax_obtener_tabla_numericos/param:1616584295937/origen:1d/fecha_ini:{fecha_ini}-00-00/fecha_fin:{fecha_fin}-00-00/zoom_ini:{fecha_ini}-00-00/zoom_fin:{fecha_fin}-00-00/_senal:E_36UI__15|E_36UI__15|E_36UI__15/_valor:MED|MAX|MIN/ver_detalle:1/alto:753&_=1616584295938'.format(fecha_ini=fecha_ini, fecha_fin=fecha_fin), verify=False, stream=True)
Radiacion=requests.get('https://saihtajo.chtajo.es/libs/sedh_lite/ajax.php?url=/sedh/ajax_obtener_tabla_numericos/param:1616584327777/origen:1d/fecha_ini:{fecha_ini}-00-00/fecha_fin:{fecha_fin}-00-00/zoom_ini:{fecha_ini}-00-00/zoom_fin:{fecha_fin}-00-00/_senal:E_36UI__16|E_36UI__16|E_36UI__16/_valor:MED|MAX|MIN/ver_detalle:1/alto:946&_=1616584327777'.format(fecha_ini=fecha_ini, fecha_fin=fecha_fin), verify=False, stream=True)
Temperatura=requests.get('https://saihtajo.chtajo.es/libs/sedh_lite/ajax.php?url=/sedh/ajax_obtener_tabla_numericos/param:1616584360522/origen:1d/fecha_ini:{fecha_ini}-00-00/fecha_fin:{fecha_fin}-00-00/zoom_ini:{fecha_ini}-00-00/zoom_fin:{fecha_fin}-00-00/_senal:E_36UI__13|E_36UI__13|E_36UI__13/_valor:MED|MAX|MIN/ver_detalle:1/alto:946&_=1616584360523'.format(fecha_ini=fecha_ini, fecha_fin=fecha_fin), verify=False, stream=True)
VelocidadViento=requests.get('https://saihtajo.chtajo.es/libs/sedh_lite/ajax.php?url=/sedh/ajax_obtener_tabla_numericos/param:1616584397234/origen:1d/fecha_ini:{fecha_ini}-00-00/fecha_fin:{fecha_fin}-00-00/zoom_ini:{fecha_ini}-00-00/zoom_fin:{fecha_fin}-00-00/_senal:E_36UI__11|E_36UI__11|E_36UI__11/_valor:MED|MAX|MIN/ver_detalle:1/alto:753&_=1616584397234'.format(fecha_ini=fecha_ini, fecha_fin=fecha_fin), verify=False, stream=True)






Variables=[m, cota, DireccionViento, Humedad, Pluviometro, Presion, Radiacion, Temperatura, VelocidadViento]

def introducirdatos(nombre, med, max, min, date, ValMedio, ValMax, ValMin):
    i=0
    for m in ValMedio:
        tiempo = int(time.mktime(datetime.datetime.strptime(date[i], "%d/%m/%Y").timetuple()))
        if m != "":
            json_body = []
            informacion = {'measurement': nombre, 'tags': {'Mancomunidad': 'Ahigal'},
                           'fields': {med: float(m.replace(",", ".")),
                                      max: float(ValMax[i].replace(",", ".")),
                                      min: float(ValMin[i].replace(",", "."))}, 'time': tiempo}
            json_body.append(informacion)
            datoinside = client.write_points(json_body, time_precision='s')
            print(json_body)
        i=i+1
x=0
for var in Variables:
    date = []
    soup=BeautifulSoup(var.content, 'html.parser')
    datostotal=soup.find_all( "td",{"class": "_lineasr"})
    fecha = soup.find_all("td", {"class": "_lineasc"})
    for r in fecha:
        date.append(r.text.strip())
    if len(datostotal)== len(fecha):
        dato=[]
        for i in datostotal:
            dato.append(i.text.strip())
    else:
        v = 0
        ValMedio = []
        ValMax = []
        ValMin = []
        while v < len(datostotal):
            ValMedio.append(datostotal[v].text.strip())
            ValMax.append(datostotal[v + 1].text.strip())
            ValMin.append(datostotal[v + 2].text.strip())
            v = v + 3
    if x==0:
        i=0
        for m in dato:
            tiempo = time.mktime(datetime.datetime.strptime(date[i], "%d/%m/%Y").timetuple())
            tiempo = int(tiempo)
            if m != "":
                json_body = []
                informacion = {'measurement': 'Pantano_Gabriel_Galan', 'tags': {'Mancomunidad': 'Ahigal'},
                               'fields': {'NivelLlenado': float(m.replace(",", "."))}, 'time': tiempo}
                json_body.append(informacion)
                datoinside = client.write_points(json_body, time_precision='s')
            i = i + 1
        x= x+1
    elif x==1:
        nombre= 'Pantano_Gabriel_Galan_Cota'
        med='Cota_Med'
        min='Cota_Min'
        max='Cota_Max'
        introducirdatos(nombre, med, max, min, date, ValMedio, ValMax, ValMin)
        x=x+1

    elif x==2:
        nombre = 'Pantano_Gabriel_Galan_DirViento'
        med = 'Viento_Med'
        min = 'Viento_Min'
        max = 'Viento_Max'
        introducirdatos(nombre, med, max, min, date, ValMedio, ValMax, ValMin)
        x=x+1
    elif x==3:
        nombre = 'Pantano_Gabriel_Galan_Humedad'
        med = 'Humedad_Med'
        min = 'Humedad_Min'
        max = 'HUmedad_Max'
        introducirdatos(nombre, med, max, min, date, ValMedio, ValMax, ValMin)
        x = x + 1
    elif x==4:
        nombre = 'Pantano_Gabriel_Galan_Pluviometro'
        med = 'Pluviometro_Med'
        min = 'Pluviometro_Min'
        max = 'PLuviometro_Max'
        introducirdatos(nombre, med, max, min, date, ValMedio, ValMax, ValMin)
        x = x + 1
    elif x==5:
        nombre = 'Pantano_Gabriel_Galan_Presion'
        med = 'Presion_Med'
        min = 'Presion_Min'
        max = 'Presion_Max'
        introducirdatos(nombre, med, max, min, date, ValMedio, ValMax, ValMin)
        x = x + 1
    elif x==6:
        nombre = 'Pantano_Gabriel_Galan_Radiacion'
        med = 'Radiacion_Med'
        min = 'Radiacion_Min'
        max = 'Radiacion_Max'
        introducirdatos(nombre, med, max, min, date, ValMedio, ValMax, ValMin)
        x = x + 1
    elif x==7:
        nombre = 'Pantano_Gabriel_Galan_TempAmbiente'
        med = 'Temperatura_Med'
        min = 'Temperatura_Min'
        max = 'Temperatura_Max'
        introducirdatos(nombre, med, max, min, date, ValMedio, ValMax, ValMin)
        x = x + 1
    elif x==8:
        nombre = 'Pantano_Gabriel_Galan_VelViento'
        med = 'TVelViento_Med'
        min = 'VelViento_Min'
        max = 'VelViento_Max'
        introducirdatos(nombre, med, max, min, date, ValMedio, ValMax, ValMin)
