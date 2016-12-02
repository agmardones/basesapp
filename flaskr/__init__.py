#!/usr/bin/python3
# -*- coding: latin-1 -*-
import os
import sys
import psycopg2
import json
from bson import json_util
from pymongo import MongoClient
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash


def create_app():
    app = Flask(__name__)
    return app

app = create_app()

# REPLACE WITH YOUR DATABASE NAME
MONGODATABASE = "entrega4"
MONGOSERVER = "localhost"
MONGOPORT = 27017
client = MongoClient(MONGOSERVER, MONGOPORT)
mongodb = client[MONGODATABASE]

"""
POSTGRESDATABASE = "entrega4"
POSTGRESUSER = "administrator"
POSTGRESPASSWORD = "s95Rk*Tb8"
postgresdb = psycopg2.connect("dbname = {} user = {}".format(POSTGRESDATABASE, POSTGRESUSER))
"""

#Cambiar por Path Absoluto en el servidor
QUERIES_FILENAME = '/var/www/flaskr/queries'


@app.route("/")
def home():
    with open(QUERIES_FILENAME, 'r', encoding='utf-8') as queries_file:
        json_file = json.load(queries_file)
        pairs = [(x["name"],
                  x["database"],
                  x["description"],
                  x["query"]) for x in json_file]
        return render_template('file.html', results=pairs)


@app.route("/mongo")
def mongo():
    query = request.args.get("query")
    results = eval('mongodb.'+query)
    results = json_util.dumps(results, sort_keys=True, indent=4)
    name = 'Matias'
    trai = request.values.get('fname')
    if "find" in query:
        return render_template('mongo.html', results=results, name=name, name2=trai)
    else:
        return "ok"


@app.route("/postgres")
def postgres():
    query = request.args.get("query")
    cursor = postgresdb.cursor()
    cursor.execute(query)
    r = cursor.fetchall()
    results = [[a for a in result] for result in r]
    print(results)
    return render_template('postgres.html', results=results)


@app.route("/example")
def example():
    return render_template('example.html')


@app.route("/receptor")
def receptor():
    consulta = request.args.get("name")
    if consulta == "Consulta1":
        name = request.args.get("fname")
        users = mongodb.users.find({'name': '{}'.format(name)})
        user = users.next()
        userid = user["id"]
        msgs = mongodb.messages.find({'sender': userid})
        results = json_util.dumps(msgs, sort_keys=True, indent=4)
        return render_template('receptor.html', con=consulta, name=name, lname=results)
    if consulta == "Consulta2":
        name1 = request.args.get("name1")
        name2 = request.args.get("name2")
        users1 = mongodb.users.find({'name': '{}'.format(name1)})
        users2 = mongodb.users.find({'name': '{}'.format(name2)})
        user1 = users1.next()
        user2 = users2.next()
        user1id = user1["id"]
        user2id = user2["id"]
        msgs12 = mongodb.messages.find({'sender': user1id, 'receptant': user2id})
        msgs21 = mongodb.messages.find({'sender': user2id, 'receptant': user1id})
        results1 = json_util.dumps(msgs12, sort_keys=True, indent=4)
        results2 = json_util.dumps(msgs21, sort_keys=True, indent=4)
        return render_template('receptor.html', con=consulta, results1=results1, results2=results2)


@app.route("/filtro")
def filtro():
    msg12 = request.args.get("fecha1")
    msg21 = request.args.get("fecha2")
    return render_template('fechas.html', a=msg12, b=msg21)

if __name__ == "__main__":
    app.run()
