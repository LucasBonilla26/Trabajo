from __future__ import absolute_import, division, print_function, unicode_literals
from zato.server.service import Service
import rethinkdb as rdb
from rethinkdb.errors import ReqlDriverError
import json
import re

class AccessPointsToDb(Service):

   def connectToDb(self):
      r = rdb.RethinkDB()
      r.connect('10.253.247.17', 28015, 'smartpolitech').repl()

   def insertDataIntoTable(self, table, data):
      r = rdb.RethinkDB()
      tableObject = r.table(table)
      result = tableObject.insert({"created_at": r.now(), "data": data}).run()
      return result

   def handle(self):
      r = rdb.RethinkDB()
      try:
         # Connect to the database
         self.connectToDb()

         # Fetch connection to Access Points
         aps = self.outgoing.plain_http.get('Access Points')

         #request = {'cust_id':1, 'name':'Foo Bar'}
         response = aps.conn.get(self.cid)

         # Insert response into the database
         aps = json.loads(response.text)

         for ap in aps:
            self.insertDataIntoTable("UEXCC_APS", ap)

         #self.logger.info(result)

      except ReqlDriverError:
         self.response.payload = "Couldn't connect to the data base"
      except ValueError:
         self.response.payload = "Json exception"
      except:
         self.response.payload = "Generic Exception"