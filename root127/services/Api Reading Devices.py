from __future__ import absolute_import, division, print_function, unicode_literals
from zato.server.service import Service
import rethinkdb as r
from rethinkdb.errors import ReqlDriverError
import json
import re


class ApiReadingDevices(Service):

    maxConnections = 100
    minutesToResetCounter = 1

    class SimpleIO:
        input_required = ("json",)
        #output_required

    def connectToDb(self):
        r.connect('10.253.247.17', 28015, 'smartpolitech').repl()

    def existDevice(self, device):
        if r.table("devices").filter(r.row['id'].match(device)).count().run() > 0:
            return True
        else:
            return False

    def apiKeyPermission(self, apiKey):
        if r.table("access_control").filter(r.row['api_key'].match(apiKey)).count().run() > 0:
            return True
        else:
            return False

    def maxRequestsReached(self, apiKey):
        if r.table("access_control").filter( (r.row.has_fields("api_key", "counter_access", "last_access")) & r.row['api_key'].match(apiKey) & ((r.now() - r.row['last_access']) / 60 > self.minutesToResetCounter) ).count().run() > 0:
	    r.table("access_control").filter(r.row['api_key'].match(apiKey)).update({"last_access": r.now(), "counter_access" : 0}).run()
            return False
        elif r.table("access_control").filter( (r.row.has_fields("api_key", "counter_access", "last_access")) & r.row['api_key'].match(apiKey) & ((r.now() - r.row['last_access']) / 60 < self.minutesToResetCounter) & (r.row["counter_access"] < self.maxConnections)).count().run() > 0:
	    r.table("access_control").filter(r.row['api_key'].match(apiKey)).update({"counter_access" : r.row["counter_access"] + 1}).run()
            return False
	else:
	    return True

    def queryToDevices(self, input):

        rows = r.table("devices").run()

	result = []
	for row in rows:
	   result.append( {"device" : row["id"], "description" : row["Description"]})

	return json.dumps(result)


    def handle(self):
        try:
            input  = json.loads(self.request.input.json)
	    self.connectToDb()


            if 'info' not in input:
		self.response.payload = {"error": "Invalid JSON structure"}
	    elif 'api_key' not in input["info"]:
                self.response.payload = {"error": "Invalid JSON structure. Missing api_key"}
            elif self.apiKeyPermission(input["info"]["api_key"]) == False:
		self.response.payload = {"error": "Invalid Api Key"}
	    elif self.maxRequestsReached(input["info"]["api_key"]) == True:
	 	self.response.payload = {"error": "Max connections exceded, please try later"}
	    else:
		self.response.payload = self.queryToDevices(input)


        except ValueError:
            self.response.payload = "No se ha podido parsear el json"
        except ReqlDriverError:
            self.response.payload = "No se ha realizado la conexion"
        #except:
        #    self.response.payload = "Excepcion generica"
