from flask import Flask, jsonify, request
import uuid
import MongoManager

app =  Flask(__name__)
"""
nombre
Edad
password
token
"""
__mongo = MongoManager.MongoManager.getInstance()

@app.route('/add-user/', methods = ['POST'])
def add_user():
    #obtener request
    request_data = request.get_json()
    if validateRequest(request_data):
        print("Request Valido!")
        try:
            token = generateToken()
            db = __mongo["TiendaComics"]
            table = db["Users"]
            result = table.find_one({"name": request_data['name']})
            if result:
                #usuario ya existe
                response = {
                    "code": 500,
                    "message": 'Nombre de usuario ya esta en uso.'
                }
                return jsonify(response)
            else:
                mydict = {"name": request_data['name'],
                          "age": request_data['age'],
                          "password": request_data['password'],
                          "token": token
                          }
                result = table.insert_one(mydict)
                response = {
                    "code": 200,
                    "message": 'Succes'
                }
                return jsonify(response)
        except Exception as e:
            print(e)
            response = {
                "code": 500,
                "message": 'Error en la petición'
            }
            return jsonify(response)
    else:
        print('Request invalido')
        response = {
                "code": 500,
                "message": 'Verifica tu request!'
            }
        return jsonify(response)

@app.route('/users/', methods = ['POST'])
def get_user():
    request_data = request.get_json()
    if validateRequestLoggin(request_data):
        print("Request Valido!")
        try:
            db = __mongo["TiendaComics"]
            table = db["Users"]
            result = table.find_one({"name": request_data['name']})
            if result:
                passwordcheck = result['password']
                if passwordcheck == request_data['password']:
                    response = {
                        "code": 200,
                        "message": 'Credenciales validas',
                        "data": {
                            "id": str(result['_id']),
                            "name": result['name'],
                            "age": result['age'],
                            "token": result['token']
                        }

                    }
                    return jsonify(response)
                else:
                    response = {
                        "code": 500,
                        "message": 'Credenciales invalidas'
                    }
                    return jsonify(response)
            else:
                response = {
                    "code": 500,
                    "message": 'Credenciales invalidas'
                    }
            return jsonify(response)
        except Exception as e:
            print(e)
            response = {
                "code": 500,
                "message": 'Error en la petición'
            }
            return jsonify(response)
    else:
        print('Request invalido')
        response = {
                "code": 500,
                "message": 'Verifica tu request!'
            }
        return jsonify(response)

def validateRequest(request_data):
    if request_data['name'] is None or request_data['age'] is None or request_data['password'] is None:
        return False
    else:
        return True
def validateRequestLoggin(request_data):
    if request_data['name'] is None or request_data['password'] is None:
        return False
    else:
        return True
def generateToken():
    token = uuid.uuid4()
    print(token.hex)
    return token.hex

if __name__ == '__main__':
    app.run(host="0.0.0.0", port= 4000, debug = True)