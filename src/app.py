"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for  # type: ignore
from flask_cors import CORS # type: ignore
# from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
from utils import generate_sitemap
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

jackson_family = FamilyStructure('Jackson')

# # Handle/serialize errors like a JSON object
# @app.errorhandler(APIException) # type: ignore
# def handle_invalid_usage(error):
#     return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Obtener GET todos los miembros de la familia
@app.route('/members', methods=['GET'])
def get_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

# Recupera solo un miembro id == member_id
@app.route('/member/<int:id>', methods=['GET'])
def get_members_id(id):
    member = jackson_family.get_member(id)
    return jsonify(member), 200

#  Añadir (POST) un miembro
@app.route('/member/', methods=['POST'])
def post_add_member():
   request_body = request.json # Me guardo el member que viene en el body del mensaje en la variable "request_body"
   jackson_family.post_add_member(request_body) # Llamo a la funcion "post_add_member" de la clase "jackson_family"
   return jsonify(jackson_family.get_all_members()), 200 # Retorno el listado de todo los members incluido el nuevo añadido
    # member = post_add_member(jackson_family)
    # jackson_family.append(request)

@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member_id(id):
    jackson_family.delete_member(id)
    return jsonify ('done: true'), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000)) # type: ignore
    app.run(host='0.0.0.0', port=PORT, debug=True)
