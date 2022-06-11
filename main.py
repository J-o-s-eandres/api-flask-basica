from flask import Flask,jsonify,request
from data import users

#levantar servicio
app = Flask(__name__)

#GET
@app.route('/',methods=['GET'])
def get_users():#lista a todos los usuarios
    return jsonify(users)

@app.route('/<int:id_user>',methods=['GET'])
def get_user(id_user):#lista a todos los usuarios hasta que le pases el /num_id del usuario que buscas 
    return jsonify(
        [i for i in users if i['id'] == id_user]
    )

#POST 
@app.route('/', methods= ['POST'])
def add_user():
    new_user={
        "id": request.json['id'], 
        "name":  request.json['name'],
        "apellido": request.json['apellido'],
        "edad": request.json['edad'],
        "correo": request.json['correo'],
        "status": request.json['']       
        }

    users.append(new_user)
    return jsonify({"Mensaje": "Usuario agregado satisfactoriamente","Nuevo Usuario":users})

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
        "status": request.json['']       
        }

        users.append(obj_user)

        return jsonify({
            "Mensaje" : "Usuario actualizado",
            "Usuario" : obj_user
        })

    
#DELETE
@app.route('/<int:id_user>',methods= ['DELETE'])
def delete_user(id_user):
    obj_user = [i for i in users if i ['id']==id_user]


    if len(obj_user)> 0:
        users.remove(obj_user[0])

        return jsonify({
            "Mensaje" : "Usuario Eliminado",
            "Usuarios" : users
        })
    return "Usuario no encontrado"

def main():
    app.run(debug=True, port=8080)#para poder debuguear



#evaluar si estoy en el archivo principal , y si lo estoy llamar a main
if __name__ == '__main__':
    main()