# stdlib
from json import dumps

# Zato
from zato.server.service import Service

class ReadAccessPoints(Service):
    def handle(self):

        # Fetch connection to Access Points
        aps = self.outgoing.plain_http.get('Access Points')

	request = {'cust_id':1, 'name':'Foo Bar'}
        response = aps.conn.get(self.cid, request)

        self.logger.info(response.headers['content-type'])
        self.logger.info(response.text)

        # Grab the Access Points info ..
        #response = accessPoints.conn.get(self.cid, "a:a")



        #self.logger.info('Customer details: {}'.format(response.text))

        # And return response to the caller
        self.response.payload = response.text
