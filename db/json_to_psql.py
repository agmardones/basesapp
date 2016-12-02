import psycopg2
import json

conn = psycopg2.connect("dbname = hola user = andres")
cur = conn.cursor()
# Setup, para no cargar siempre lo mismo
cur.execute("DROP TABLE messages")
cur.execute("DROP TABLE users")
cur.execute("CREATE TABLE messages (date date, sender int, receptant int, lat int, long int, message varchar(1000));")
cur.execute("CREATE TABLE users (name varchar(30), id int, age int, description varchar(1000));")

# File load
m = open("messages.json", "r")
u = open("users.json", "r")
data = json.load(m)
data_u = json.load(u)

# ---- Insertion ----
# Messages table head: (date | sender | receptant | lat | long | message)
query_template = "INSERT INTO messages VALUES({}, {}, {}, {}, {}, {})"

for i in range(len(data)):
	lat = int(data[i]["lat"])
	lon = int(data[i]["long"])
	recept = int(data[i]["receptant"])
	sender = int(data[i]["sender"])
	deit = "'{}'".format(str(data[i]["date"]))
	msg = "'{}'".format(str(data[i]["message"]))
	cur.execute(query_template.format(deit, sender, recept, lat, lon, msg))

# Messages table head: (name | id | age | description
query_template = "INSERT INTO users VALUES({}, {}, {}, {})"

for i in range(len(data_u)):
	name = "'{}'".format(str(data_u[i]["name"]))
	_id = int(data_u[i]["id"])
	age = int(data_u[i]["age"])
	descr = "'{}'".format(str(data_u[i]["description"]))
	cur.execute(query_template.format(name, _id, age, descr))

# Commit changes
conn.commit()
