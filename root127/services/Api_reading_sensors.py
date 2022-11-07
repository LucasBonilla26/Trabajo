from __future__ import absolute_import, division, print_function, unicode_literals
from zato.server.service import Service
import rethinkdb as rdb
from rethinkdb.errors import ReqlDriverError
import json
import re


class ApiReadingSensors(Service):

    maxConnections = 100
    minutesToResetCounter = 1
    limit = 1500


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

    def apiKeyPermission(self, apiKey):
        r = rdb.RethinkDB()
        if r.table("access_control").filter(r.row['api_key'].match(apiKey)).count().run() > 0:
            return True
        else:
            return False

    def maxRequestsReached(self, apiKey):
        r = rdb.RethinkDB()
        if r.table("access_control").filter( (r.row.has_fields("api_key", "counter_access", "last_access")) & r.row['api_key'].match(apiKey) & ((r.now() - r.row['last_access']) / 60 > self.minutesToResetCounter) ).count().run() > 0:
	    r.table("access_control").filter(r.row['api_key'].match(apiKey)).update({"last_access": r.now(), "counter_access" : 0}).run()
            return False
        elif r.table("access_control").filter( (r.row.has_fields("api_key", "counter_access", "last_access")) & r.row['api_key'].match(apiKey) & ((r.now() - r.row['last_access']) / 60 < self.minutesToResetCounter) & (r.row["counter_access"] < self.maxConnections)).count().run() > 0:
	    r.table("access_control").filter(r.row['api_key'].match(apiKey)).update({"counter_access" : r.row["counter_access"] + 1}).run()
            return False
	else:
	    return True

    def queryToDevices(self, input):
        r = rdb.RethinkDB()

	fromDate = None
        toDate = None


	if 'from' in input["info"]:
	   fromDate = input["info"]["from"]

	if 'to' in input["info"]:
           toDate = input["info"]["to"]

        #if 'orderBy' in input["info"]
        #   orderBy = input["info"]["orderBy"]


	if fromDate is not None and toDate is not None:
	   rows = r.table(input["info"]["device"]).order_by(index=r.desc('created_at')).filter((r.row["created_at"].to_iso8601() >= fromDate) & (r.row["created_at"].to_iso8601() <= toDate) ).limit(self.limit).run()
        else:
           #rows = r.table(input["info"]["device"]).limit(self.limit).order_by('created_at').run()
           rows = r.table(input["info"]["device"]).order_by(index=r.desc('created_at')).limit(self.limit).run()


	result = []
	for row in rows:
	   result.append( {"created_at" : row["created_at"].isoformat(), "data" : row["data"]})

	return json.dumps(result)




    def validDateRange(self, input):

	p = re.compile('^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\\.[0-9]+)?(Z)?$')

	if 'from' in input["info"] and not p.match(input["info"]["from"]):
           return False
        if 'to' in input["info"] and not p.match(input["info"]["to"]):
           return False

        return True




    def handle(self):
        try:
            input  = json.loads(self.request.input.json)
	    self.connectToDb()


            if 'info' not in input:
		self.response.payload = {"error": "Invalid JSON structure"}
            elif 'device'not in input["info"]:
                self.response.payload = {"error": "Invalid JSON structure. Missing device table"}
	    elif 'api_key' not in input["info"]:
                self.response.payload = {"error": "Invalid JSON structure. Missing api_key"}
            elif self.apiKeyPermission(input["info"]["api_key"]) == False:
		self.response.payload = {"error": "Invalid Api Key"}
	    elif self.maxRequestsReached(input["info"]["api_key"]) == True:
	 	self.response.payload = {"error": "Max connections exceded, please try later"}
	    elif self.existDevice(input["info"]["device"]) == False:
                self.response.payload = {"error": "Invalid device table"}
	    elif self.validDateRange(input) == False:
		self.response.payload = {"error": "Invalid date format. It should be in iso8601. Example: 2018-02-07T12:00:52"}
	    else:
		self.response.payload = self.queryToDevices(input)


        except ValueError:
            self.response.payload = "No se ha podido parsear el json"
        except ReqlDriverError:
            self.response.payload = "No se ha realizado la conexion"
        #except:
        #    self.response.payload = "Excepcion generica"
