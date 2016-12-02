from pymongo import MongoClient
import sys

MONGODATABASE = "entrega4"
MONGOSERVER = "localhost"
MONGOPORT = 27017
client = MongoClient(MONGOSERVER, MONGOPORT)
db = client[MONGODATABASE]

args = sys.argv[1:]
users = db.users.find({'name': '{} {}'.format(*args)})
try:
	user = users.next()
	userid = user["id"]
	msgs = db.messages.find({'sender': userid})
	for m in msgs:
		pass
		print(m)
except StopIteration:
	print("Probablemente una consulta vacía")