from pymongo import MongoClient
from bson import json_util
import time
import sys

MONGODATABASE = "entrega4"
MONGOSERVER = "localhost"
MONGOPORT = 27017
client = MongoClient(MONGOSERVER, MONGOPORT)
db = client[MONGODATABASE]

args1 = sys.argv[1:3] # Nombre del primero
args2 = sys.argv[3:] # Nombre del segundo
users1 = db.users.find({'name': '{} {}'.format(*args1)})
users2 = db.users.find({'name': '{} {}'.format(*args2)})
try:
	user1 = users1.next()
	user2 = users2.next()
	user1id = user1["id"]
	user2id = user2["id"]
	msgs12 = db.messages.find({'sender': user1id, 'receptant': user2id})
	msgs21 = db.messages.find({'sender': user2id, 'receptant': user1id})
	"""
	Supongamos que nuestro bello y querido usuario quiere buscar entre las fechas
	2015-04-17 y 2016-12-01
	(Habría que poner un if pq podría no querer filtrar por fechas)
	"""
	inf = time.strptime("2015-04-17", "%Y-%m-%d") # Límite inferior
	sup = time.strptime("2016-12-01", "%Y-%m-%d") # Límite superior
	"""
	Supongamos tambien que quiere los que están en la posición:
	latitud = -18.483333
	longitud = -70.333333
	"""
	lat = -18.483333 
	lon = -70.333333
	to_send = []
	for m in msgs12:
		if inf < time.strptime(m["date"], "%Y-%m-%d") < sup:
			to_send.append(m)
		if float(m["long"]) == lon and float(m["lat"]) == lat: pass
	for m in msgs21:
		if inf < time.strptime(m["date"], "%Y-%m-%d") < sup: 
			to_send.append(m)
		if float(m["long"]) == lon and float(m["lat"]) == lat: pass

	results = json_util.dumps(to_send, sort_keys=True, indent=4)
	print(results)
except StopIteration:
	print("Probablemente una consulta vacía")