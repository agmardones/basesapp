from pymongo import MongoClient
import sys

MONGODATABASE = "entrega4"
MONGOSERVER = "localhost"
MONGOPORT = 27017
client = MongoClient(MONGOSERVER, MONGOPORT)
db = client[MONGODATABASE]
phrase = "" # db.messages.find({"$text": {"$search": "\"{}\"".format(phrase)}});
banned_words = ["despido", "saludos"]
if phrase:
	cur = db.messages.find({"$text": {"$search": "\"{}\"".format(phrase)}});
else:
	cur = db.messages.find();

will_print = True
to_send = []
for msg in cur:
	for w in banned_words:
		if w in msg["message"]:
			will_print = False
	if will_print:
		to_send.append(msg)
	will_print = True

results = json_util.dumps(to_send, sort_keys=True, indent=4)

