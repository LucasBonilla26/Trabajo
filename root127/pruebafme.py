from __future__ import absolute_import, division, print_function, unicode_literals
import time
from influxdb import InfluxDBClient
import json
from py2neo import Graph, Node
from py2neo import Node, Relationship
import sys, time
#from neo4j import GraphDatabase
import csv
import datetime



influxhost='10.253.247.18'
port=8086
username='r0b0l4b'
password='alwayssmarter54'
database='sensors'
neo='neo4j://158.49.112.122:7687',
neouser="Smart"
neopass="Politech"
Tipo_Sensor="temp"
graph = Graph("bolt://158.49.112.122:7687", auth=(neouser, neopass))
results = graph.run(
                    "MATCH (a:Room),(b:Device) WHERE $type in b.type and (a)-[:HAS]->(b) "
                    "RETURN a as Sala, b as Nombre_Sensor",
                    type=Tipo_Sensor).data()
print(results)
