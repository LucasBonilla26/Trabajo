import os, time, datetime
from colored import fg, bg
import telepot
from telepot.loop import MessageLoop
from emoji import demojize, emojize
import traceback
import xlrd
import csv
import os
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import openpyxl
from os import remove
from influxdb import InfluxDBClient
import json

client = InfluxDBClient(host='158.49.112.127', port=8086)
client.switch_database('CASAR')
parent_folder = os.path.abspath(os.path.dirname(__file__))
documents_folder = os.path.join(parent_folder, "documents")

if not os.path.exists(documents_folder):
    os.makedirs(documents_folder)

#log
def printLog(text):
    log = open("log", "a+")
    log.write("@#$%&[" + str(datetime.datetime.now()) + "]:" + text + "\n")
    log.close()




#counter
count_request = 0

# Color and background reset
CR = fg(15) + bg(0)




##########################  Token  ##########################
try:
    token_path = os.path.join(parent_folder, "token")
    token = open(token_path).readline().replace("\n", "")
    print("Token encontrado:  \""+ fg(2) + token + fg(15) + "\"")
except:
    print(fg(15) + "[!]" + fg(1) + " Token no encotrado." + fg(15))



##########################  Funciones  ##########################

def ghc(seed):
    """
    GetHashedColored
    Devuelve el numero pintado de un color aleatorio en funcion de si mismo.
    Cada numero devuelve siempre el mismo color.

    El resultado devuelto es un String listo para poner en el print.
        color + str(numero) + colorReset

    El rango de color es de 256 colores.
    """
    seed = int(seed)
    color = (seed % 255) + 1
    back = 0

    # Si es oscuro, ponemos el fondo claro
    if color == 16:
        back = 250
    elif color >= 232 and color <= 240:
        back = 15

    try:
        return fg(color) + bg(back) + str(seed) + fg(15) + bg(0)
    except:
        printLog("bad color " + str(seed))
        return fg(0) + bg(9) + str(seed) + fg(15) + bg(0)


def xlsxtocsv (file, ruta, client):
    xlsx = openpyxl.load_workbook(file)# Cargamos
    for i in xlsx.sheetnames:
        nombre=i
        sheet=xlsx[i]
        data=sheet.rows
        filepath = ruta + '/' + i + "_" + str(datetime.datetime.now()) + '.csv'
        with open(filepath, "w+") as csvfile:
            a = 0
            for row in data:
                l = list(row)
                if a == 0:
                    fieldnames = []
                    num_campos=len(l)
                    for i in range(len(l)):
                        fieldnames.append(str(l[i].value))
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    a = +1
                    dic = dict.fromkeys(fieldnames, 1)
                    dicmed=dict.fromkeys(fieldnames[1:],1)
                else:
                    for i in range(len(l)):
                        dic[fieldnames[i]]=str(l[i].value)
                    writer.writerow(dic)
        with open(filepath) as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',')
            x = 0
            for row in csv_reader:
                if x == 0 or row[1] == '#N/A':
                    x = x + 1
                else:
                    for j in range(num_campos):
                        if j==0:
                            fecha_separado= row[j].split(sep=' ')
                            tiempo = time.mktime(datetime.datetime.strptime(fecha_separado[0], "%Y-%m-%d").timetuple())
                            tiempo = int(tiempo)
                        else:
                            dicmed[fieldnames[j]]=float(row[j])
                    json_body = []
                    informacion = {'measurement': "Casar:" + nombre, 'tags': {'Localidad': 'Casar'},
                                   'fields': dicmed, 'time': tiempo}
                    json_body.append(informacion)
                    print(json_body)
                    datoinside = client.write_points(json_body, time_precision='s')

    ## close the csv file
    return filepath

##########################  Msg Loop  ##########################

def on_chat_message(msg):
    """ Funcion que se ejecuta cuando el bot recibe un mensaje. """
    content_type, chat_type, chat_id = telepot.glance(msg)

    if content_type == "text":
        if msg["text"] == "/start":
            my_bot.sendMessage(chat_id=chat_id, text=emojize("Todo esta preparado para que envies el archivo :thumbs_up:"))



    if content_type == "document":
        document_dict = msg["document"]
        document_id = document_dict["file_id"]
        document_name = document_dict["file_name"]
        document_size = document_dict["file_size"]


        print(ghc(chat_id) + " - " + str(document_name) + " (size: " + str(document_size/1000) + " KB)", end='  \t')

        try:
            # Aqui va lo que hacemos con el mensaje

            # Descargamos el archivo
            nombre=document_name + "_" + str(datetime.datetime.now())
            dest_docu_path = os.path.join(documents_folder, nombre)
            my_bot.download_file(document_id, dest_docu_path)
            old_file=os.path.join(documents_folder, nombre)
            new_file=os.path.join(documents_folder,'intermedio.xlsx')
            os.rename(old_file, new_file)
            pathnewfile=xlsxtocsv(new_file, documents_folder, client)





            print(fg(10) + "✓")
        except Exception as e:
            print(fg(1)  + "✗")
            printLog(traceback.format_exc())
            # Enviar excepcion al admin
            sendMeTheLog(my_bot, content_type, chat_type, chat_id, justLast=True, initText=emojize(":warning: Error de " + str(chat_id) + ":\n\n"))
            # Enviar mensaje al user
            my_bot.sendMessage(chat_id=chat_id, text=emojize("Ups! Parece que algo ha salido mal :face_screaming_in_fear:"))
















##########################  log control  ##########################

def sendMeTheLog(my_bot, content_type, chat_type, chat_id, justLast = False, initText = emojize(":page_facing_up: Full log:\n\n")):
    """ Enviamos el log entero al admin. """

    # Si el usuario es admin
    if checkIfAdmin(chat_id):
        # Obtenemos el texto del log y enviamos
        if justLast:
            log_path = os.path.join(parent_folder, "log")
            log = open(log_path, "r").read()
            log = log[log.rfind("@#$%&"):]
            my_bot.sendMessage(chat_id, text=initText + log, reply_markup=None)
        else:
            log_path = os.path.join(parent_folder, "log")
            my_bot.sendMessage(chat_id, text=initText + open(log_path, "r").read(), reply_markup=None)
    else:
        msg=emojize(":prohibited: No tienes permiso para hacer eso :prohibited:")
        my_bot.sendMessage(chat_id, text=msg, reply_markup=None)


def sendMeJustLastLogEntry(my_bot, content_type, chat_type, chat_id):
    sendMeTheLog(my_bot, content_type, chat_type, chat_id, justLast=True, initText=emojize(":scroll: Ultima entrada:\n\n"))


def checkIfAdmin(chat_id):
    """ Dice si el chat_id es admin """
    # Obtenemos el id del admin
    admin_id_path = os.path.join(parent_folder, "admin_id")
    admin_id = open(admin_id_path, "r").read()

    # Si el usuario es admin
    return str(chat_id) in str(admin_id)






##########################  Inicio  ##########################

my_bot = telepot.Bot(token)


MessageLoop(my_bot, {'chat': on_chat_message}).run_as_thread()
print('Listening ...')

while True:
    time.sleep(10)
