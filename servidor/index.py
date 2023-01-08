from bson import json_util
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_cors import CORS, cross_origin
from flask import Flask, request, Response, jsonify

app = Flask(__name__)
CORS(app)
#Conceccion a la base de datos
app.config['MONGO_URI'] = "mongodb://127.0.0.1:27018,127.0.0.1:27019/pydistribuidas?replicaSet=tocset"
mongo = PyMongo(app)

# CREAR USUARIOS
@cross_origin
@app.route('/users', methods=['POST'])
def create_user():
  print(request.json)
  username = request.json['username']
  password = request.json['password']
  email = request.json['email']

  if username and email and password:
    mongo.db.users.insert_one({
      'username': username, 'email': email, 'password': password
    })
    response = {
      'username': username,
      'password': password
    }
    return response
  else:
    {'message': 'ocurrio un error al crear'}
  return {'message': 'usurario creado'}

#OBETENER USUARIOS
@app.route('/users', methods=['GET'])
def get_users():
  usuarios = mongo.db.users.find()
  response = json_util.dumps(usuarios)
  return Response(response, mimetype='aplications/json')

#OBTENER UN USUARIO
@app.route('/users/<id>', methods=['GET'])
def get_user(id):
  user = mongo.db.users.find_one({'_id': ObjectId(id)})
  response = json_util.dumps(user)
  return Response(response, mimetype='aplications/json')

#ELIMINAR UN USUARIO
@app.route('/users/<id>', methods=['DELETE'])
def delele_user(id):
  mongo.db.users.delete_one({'_id': ObjectId(id)})
  response = jsonify({ 'message': 'Usuario eliminado'})
  return response

#ACTUALIZA  UN USUARIO
@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
  username = request.json['username']
  password = request.json['password']
  email = request.json['email']
  if username and email and password:
    mongo.db.users.update_one({'_id': ObjectId(id)}, {'$set': {
      'username': username, 'email': email, 'password': password
    }})
    response = jsonify({
      'message': 'El usuario' + id + 'fue actualizado correctamente',
    })
    return response
  else:
    {'message': 'ocurrio un error al actualizar'}
  return {'message': 'usurario creado'}

# LEVANTAR SERVIDOR
if __name__ == "__main__":
  app.run(debug=True)