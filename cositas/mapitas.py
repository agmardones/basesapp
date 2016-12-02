from pymongo import MongoClient
import folium
import time
import sys

MONGODATABASE = "entrega4"
MONGOSERVER = "localhost"
MONGOPORT = 27017
client = MongoClient(MONGOSERVER, MONGOPORT)
db = client[MONGODATABASE]

name = " ".join(sys.argv[1:]) # Nombre
inf = time.strptime("2015-04-17", "%Y-%m-%d") # Límite inferior
sup = time.strptime("2016-12-01", "%Y-%m-%d") # Límite superior

users = db.users.find({'name': '{}'.format(name)})
try: 
	user = users.next()
	userid = user["id"]
	msgs = db.messages.find({'sender': userid})
	result = []
	for m in msgs:
		if inf < time.strptime(m["date"], "%Y-%m-%d") < sup:
			result.append(m)
	print(result)
	coordinates = [(m["lat"], m["long"]) for m in result]

except StopIteration:
	print("Probablemente una consulta vacía")

lat = [i[0] for i in coordinates]
lon = [i[1] for i in coordinates]
lat_avg = sum(lat)/len(lat)
lon_avg = sum(lon)/len(lon)

print(lat_avg, lon_avg)
location = folium.Map(location=[lat_avg, lon_avg])
for i in range(len(coordinates)):
	folium.Marker([coordinates[i][0], coordinates[i][1]], popup='Posicion {}'.format(i)).add_to(location)
location.save("../mapa.html")