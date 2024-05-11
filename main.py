import logging
from flask import Flask, jsonify, request
from data import users
from sql.operations import create_user, get_users_actives, get_user_active, delete_user

# Configurar el logger
logging.basicConfig(filename='logs/app.log',level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_users():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))

    # Obtener los usuarios activos con los valores de paginación especificados
    users = get_users_actives(page, per_page)

    if not users:
        logger.warning("No hay usuarios activos para mostrar")
        return jsonify({"message": "No hay usuarios con status 1"}), 404
    else:
        user_list = [{"id": user.id, "name": user.name, "apellido": user.apellido, "correo": user.correo, "status": user.status} for user in users]
        return jsonify(user_list)

@app.route('/<int:user_id>',methods=['GET'])
def get_user(user_id):
    try:
        user = get_user_active(user_id)

        if not user:
            logger.warning(f"No se encontró usuario con id {user_id}")
            return jsonify({"message": "No hay usuarios con ese id"}), 404
        else:
            user_data = {"id": user.id, "name": user.name, "apellido": user.apellido, "correo": user.correo, "status": user.status}
            return jsonify(user_data)
    except Exception as e:
        logger.error(f"Error al obtener usuario con id {user_id}: {str(e)}")
        return jsonify({"message": "Error al obtener usuario"}), 500

@app.route('/', methods=['POST'])
def add_user():
    try:
        data = request.json 
        if not data:
            logger.warning("No se proporcionaron datos para crear un usuario")
            return jsonify({"error": "No se proporcionaron datos"}), 400

        success = create_user(data) 
        if success:
            logger.info("Usuario agregado satisfactoriamente")
            return jsonify({"Mensaje": "Usuario agregado satisfactoriamente"}), 201
        else:
            logger.error("No se pudo agregar el usuario")
            return jsonify({"error": "No se pudo agregar el usuario"}), 500
    except Exception as e:
        logger.error(f"Error al agregar usuario: {str(e)}")
        return jsonify({"message": "Error al agregar usuario"}), 500

@app.route('/<int:id_user>', methods=['PUT'])
def update_user(id_user):
    try:
        obj_user = [i for i in users if i['id'] == id_user]

        if len(obj_user) > 0:
            users.remove(obj_user)
            obj_user = {
                "id": request.json['id'], 
                "name": request.json['name'],
                "apellido": request.json['apellido'],
                "edad": request.json['edad'],
                "correo": request.json['correo'],
                "status": request.json['status']       
            }

            users.append(obj_user)
            logger.info(f"Usuario con ID {id_user} actualizado")
            return jsonify({
                "Mensaje": "Usuario actualizado",
                "Usuario": obj_user
            })
    except Exception as e:
        logger.error(f"Error al actualizar usuario con id {id_user}: {str(e)}")
        return jsonify({"message": "Error al actualizar usuario"}), 500

@app.route('/user_delete/', methods=['PUT'])
def delete_user_route():
    try:
        if not request.json:
            logger.warning("La solicitud debe contener datos JSON")
            return jsonify({"message": "La solicitud debe contener datos JSON"}), 400

        if 'user_id' not in request.json:
            logger.warning("Se requiere 'user_id' en los datos JSON")
            return jsonify({"message": "Se requiere 'user_id' en los datos JSON"}), 400
        
        user_id = request.json['user_id']
        
        result, status_code = delete_user(user_id)
        return result, status_code
    except Exception as e:
        logger.error(f"Error en la solicitud: {str(e)}")
        return jsonify({"message": f"Error en la solicitud: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
