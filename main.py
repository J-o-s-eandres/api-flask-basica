from flask import Flask,jsonify,request
from data import users
import os

from sql.operations import create_user, get_users_actives


#levantar servicio
app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_users():
    # Obtener los valores de page y per_page de la solicitud del cliente
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))

    # Obtener los usuarios activos con los valores de paginación especificados
    users = get_users_actives(page, per_page)

    if not users:
        return jsonify({"message": "No hay usuarios con status 1"}), 404
    else:
        user_list = [{"id": user.id, "name": user.name, "apellido": user.apellido, "correo": user.correo, "status": user.status} for user in users]
        return jsonify(user_list)



@app.route('/<int:id_user>',methods=['GET'])
def get_user(id_user):#lista a todos los usuarios hasta que le pases el /num_id del usuario que buscas 
    return jsonify(
        [i for i in users if i['id'] == id_user]
    )

#POST 
@app.route('/', methods= ['POST'])
def add_user():
   data = request.json  # Obtener los datos del cuerpo de la solicitud
   if not data:
       return jsonify({"error": "No se proporcionaron datos"}), 400

   success = create_user(data)  # Llamar a la función create_user con los datos recibidos
   if success:
        return jsonify({"Mensaje": "Usuario agregado satisfactoriamente"}), 201
   else:
       return jsonify({"error": "No se pudo agregar el usuario"}), 500

#PUT 
@app.route('/<int:id_user>',methods= ['PUT'])
def update_user(id_user):

    obj_user = [i for i in users if i['id']==id_user]

    if len(obj_user) >0:
        users.remove(obj_user)
        obj_user={
        "id": request.json['id'], 
        "name":  request.json['name'],
        "apellido": request.json['apellido'],
        "edad": request.json['edad'],
        "correo": request.json['correo'],
        "status": request.json['status']       
        }

        users.append(obj_user)

        return jsonify({
            "Mensaje" : "Usuario actualizado",
            "Usuario" : obj_user
        })

    
#DELETE
@app.route('/<int:id_user>', methods=['DELETE'])
def delete_user(id_user):
    # Buscar el usuario por ID
    for user in users:
        if user['id'] == id_user:
            # Eliminar el usuario encontrado
            users.remove(user)
            return jsonify({
                "Mensaje": "Usuario Eliminado",
                "Usuarios": users
            })
    
    # Si el usuario no fue encontrado
    return "Usuario no encontrado"




#evaluar si estoy en el archivo principal , y si lo estoy llamar a main
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))