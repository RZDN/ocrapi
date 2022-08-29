from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util
from bson.objectid import ObjectId


app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost/prueba'
mongo = PyMongo(app)


@app.route('/users', methods=['GET'])
def getUsers():
    users = mongo.db.usuario.find()
    response = json_util.dumps(users)
    return Response(response, mimetype='application/json')


@app.route('/users/<id>', methods=['GET'])
def getUser(id):
    user = mongo.db.usuario.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(user)
    return Response(response, mimetype='application/json')


@app.route('/users', methods=['POST'])
def CreateUser():
    password = request.json['password']
    email = request.json['email']

    if password and email:
        hashedPassword = generate_password_hash(password)
        id = mongo.db.usuario.insert_one(
            {'email': email, 'password': hashedPassword})
        response = {
            'id': str(id.inserted_id),
            'email': email,
            'password': hashedPassword
        }
        return response
    else:
        {'message': 'error'}

    return {'message': 'received'}


if __name__ == '__main__':
    app.run(debug=True, port=4000)
