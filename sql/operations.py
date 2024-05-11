from sqlalchemy.orm import sessionmaker
from .database import engine, User
from flask import jsonify

Session = sessionmaker(bind=engine)

def create_user(data):
    session = Session()
    try:
        new_user = User(**data)
        session.add(new_user)
        session.commit()
        return True
    except Exception as e:
        print(f"Error creating user: {e}")
        session.rollback()
        return False
    finally:
        session.close()

def get_users_actives(page=1, per_page=20):
    session = Session()
    try:
        # Calcular el índice de inicio y el índice de fin para la paginación
        start_index = (page - 1) * per_page
        end_index = start_index + per_page

        # Consultar usuarios con status 1, aplicando paginación
        users = session.query(User).filter(User.status == 1).slice(start_index, end_index).all()

        return users
    except Exception as e:
        print(f"Error getting users with status 1: {e}")
        return []
    finally:
        session.close()
        
def get_user_active(user_id):
    session = Session()
    try:
        user = session.query(User).filter(User.id == user_id, User.status == 1).first()
        return user
    except Exception as e:
        print(F"Error gettins user with id: {e}")
        return None
    finally:
        session.close()

def delete_user(user_id):
    session = Session()
    
    try:
        user = get_user_active(user_id)

        if not user:
            return jsonify({"message": "No se encontró usuario para eliminar"}), 404
    
        user.status = 0
        
        session = Session()
        session.merge(user)
        session.commit()

        user_email = user.correo

        return jsonify({"message": "Usuario eliminado", "correo": user_email}), 200

    except Exception as e:
        session.rollback()
        return jsonify({"message": f"Error al eliminar el usuario: {str(e)}"}), 500

    finally:
        session.close()

def update_user(user_id, new_data):
    session = Session()

    try:
        user = get_user_active(user_id)

        if not user:
            return jsonify({"message": "No se encontró usuario para actualizar"}), 404

        # Verificar si el nuevo correo electrónico ya está registrado en otro usuario
        new_email = new_data.get("correo")
        if new_email and new_email != user.correo:
            existing_user = session.query(User).filter(User.correo == new_email).first()
            if existing_user:
                return jsonify({"message": "El correo electrónico ya está registrado en otro usuario"}), 400

        # Actualizar los datos del usuario
        user.name = new_data.get("name", user.name)
        user.apellido = new_data.get("apellido", user.apellido)
        user.correo = new_email or user.correo  # Usar el nuevo correo o mantener el existente
        session.merge(user)
        session.commit()

        user_data = {
            "id": user.id,
            "name": user.name,
            "apellido": user.apellido,
            "correo": user.correo,
            "status": user.status
        }

        return jsonify({"message": "Usuario actualizado", "usuario": user_data}), 200

    except Exception as e:
        session.rollback()
        return jsonify({"message": f"Error al actualizar el usuario: {str(e)}"}), 500

    finally:
        session.close()
