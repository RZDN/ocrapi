import flask
from flask import request, Response
from bson import json_util
import pymongo

STORIES = flask.Blueprint('stories', __name__)

myclient = pymongo.MongoClient("mongodb://3ce4e613-0ee0-4-231-b9ee:qfDSkSADTncQVX9L0T4910t4uhxe7QJpPaJCcWcNr5SYqB1EzXOZDPQz34bTXNCrdVcZ1X9ga6M4tRyepsRP7g==@3ce4e613-0ee0-4-231-b9ee.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@3ce4e613-0ee0-4-231-b9ee@")


@STORIES.route('/history', methods=['POST'])
def createHistory():
    nombre = request.json['nombre']
    apellido = request.json['apellido']
    dni = request.json['dni']
    numHistory = request.json['numHistory']
    date = request.json['date']
    sexo = request.json['sexo']

    if numHistory and date and nombre and apellido and dni and sexo:
        history = myclient.ocrapp.history.find_one(
            {'numHistory': numHistory})
        print(history)
        if (history == None):
            id = myclient.ocrapp.history.insert_one(
                {
                    'nombre': nombre,
                    'apellido': apellido,
                    'dni': dni,
                    'numHistory': numHistory,
                    'date': date,
                    'sexo': sexo})
            return {
                'message': 'registro exitoso'
            }
        else:
            return {'message': 'historia clinica ya existe'}

    return {'message': 'faltan datos'}


@STORIES.route('/history/<dni>', methods=['GET'])
def getHistoryByNumOfHistory(dni):
    history = myclient.ocrapp.history.find_one({'dni': dni})
    if (history == None):
        return {'message': 'Historia clinica no existe'}
    else:
        return Response(json_util.dumps(history), mimetype='application/json')


@STORIES.route('/history/name/<name>/<lastName>', methods=['GET'])
def getHistoryByName(name, lastName):
    history = myclient.ocrapp.history.find_one(
        {'nombre': name, "apellido": lastName})
    prueba = json_util.dumps(history)
    print(prueba)
    if (history == None):
        return {'message': 'Historia clinica no existe'}
    else:
        return Response(json_util.dumps(history), mimetype='application/json')
