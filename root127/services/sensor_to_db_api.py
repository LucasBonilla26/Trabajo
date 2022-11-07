from __future__ import absolute_import, division, print_function, unicode_literals
from zato.server.service import Service
import rethinkdb as rdb
#from rethinkdb.errors import ReqlDriverError
import json


class SensorToDbApi(Service):

    class SimpleIO:
        input_required = ("json",)
        #output_required

    def connectToDb(self):
        r = rdb.RethinkDB()
        r.connect('10.253.247.17', 28015, 'smartpolitech').repl()

    def existDevice(self, device):
        r = rdb.RethinkDB()
        if r.table("devices").filter(r.row['id'].match(device)).count().run() > 0:
            return True
        else:
            return False

    def insertDataIntoTable(self, table, data):
        r = rdb.RethinkDB()
        tableObject = r.table(table)
        result = tableObject.insert({"created_at": r.now(), "data": data}).run()

    def handle(self):
        try:
            input  = json.loads(self.request.input.json)
            device = input["info"]["device"]
            data   = input["data"][0]

            self.connectToDb()
            if self.existDevice(device):
                self.insertDataIntoTable(device, data)
                self.response.payload = "Dato insertado correctamente"
            else:
                self.response.payload ="no existe la tabla"

        except ValueError:
            self.response.payload = "No se ha podido parsear el json"
        except ReqlDriverError:
            self.response.payload = "No se ha realizado la conexion"
        #except:
        #    self.response.payload = "Excepcion generica"
