from flask import Flask,jsonify,request
from data import users
import os

from sql.operations import create_user, get_users_actives,get_user_active, delete_user

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_users():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))

    # Obtener los usuarios activos con los valores de paginación especificados
    users = get_users_actives(page, per_page)

    if not users:
        return jsonify({"message": "No hay usuarios con status 1"}), 404
    else:
        user_list = [{"id": user.id, "name": user.name, "apellido": user.apellido, "correo": user.correo, "status": user.status} for user in users]
        return jsonify(user_list)



@app.route('/<int:user_id>',methods=['GET'])
def get_user(user_id):
    
    user = get_user_active(user_id)

    if not user:
        return jsonify({"message": "No hay usuarios con ese id"}), 404
    else:
        user_data = {"id": user.id, "name": user.name, "apellido": user.apellido, "correo": user.correo, "status": user.status}
        return jsonify(user_data)


#POST 
@app.route('/', methods= ['POST'])
def add_user():
   data = request.json 
   if not data:
       return jsonify({"error": "No se proporcionaron datos"}), 400

   success = create_user(data) 
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
@app.route('/user_delete/', methods=['PUT'])
def delete_user_route():
    try:
        if not request.json:
            return jsonify({"message": "La solicitud debe contener datos JSON"}), 400

        if 'user_id' not in request.json:
            return jsonify({"message": "Se requiere 'user_id' en los datos JSON"}), 400
        
        user_id = request.json['user_id']
        
        result, status_code = delete_user(user_id)
        return result, status_code
    except Exception as e:
        return jsonify({"message": f"Error en la solicitud: {str(e)}"}), 500





#evaluar si estoy en el archivo principal , y si lo estoy llamar a main
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))