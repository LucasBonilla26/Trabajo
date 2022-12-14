#!/usr/bin/env python
from zato.server.service import Service
import requests
import json
import base64
import zlib

class Neo4jCalls(Service):
    def query(self, req):
        url = "http://158.49.112.122:7474/db/data/transaction/commit"
        headers = { "Authorization": 'Basic ' + base64.b64encode('Smart:Politech'.encode('utf-8')).decode("utf-8"),
            "X-Stream": "true",
            "Accept": "application/json; charset=UTF-8",
            "Content-Type": "application/json"}
        
        m_poly = []
        for r in req:
            poly = []
            for x in r:
                p = " ".join(list(map(lambda xx: json.dumps(xx).replace(",", " "), x)))
                poly.append(p)
            m_poly.append("(" + " , ".join(poly) + " )")


        statement = "WITH 'POLYGON({})' as polygon CALL spatial.intersects('geom',polygon) YIELD node RETURN node".format(" , ".join(m_poly))
        #return json.dumps({"result" :statement})
        #"match (n) return n","resultDataContents"
        data = { "statements": [{"statement": statement ,"resultDataContents": ["graph"]}]}
        response = requests.post(url, 
            data=json.dumps(data),
            headers=headers)
        return response.content

    def handle(self):

        data = self.request.payload
        r = self.query(json.loads(data)["query"])
        self.response.payload = base64.b64encode(zlib.compress(r))
        #self.response.payload = r