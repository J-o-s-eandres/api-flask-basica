# crud/operations.py
from sqlalchemy.orm import sessionmaker
from .database import engine, User

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

