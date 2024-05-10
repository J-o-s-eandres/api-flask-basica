from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Crear la conexión a la base de datos SQLite
engine = create_engine('sqlite:///users.db', echo=True)  # 'echo=True' imprime las consultas SQL generadas

# Crear una sesión para interactuar con la base de datos
Session = sessionmaker(bind=engine)
session = Session()

# Definir el modelo de usuario
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement = True)
    name = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    correo = Column(String, nullable=False, unique=True)
    status = Column(String,default=1, nullable=False)
    
    __maper_args__={
        'check_constraints' :[
            'status IN (0, 1)'
        ]
    }

# Crear la tabla en la base de datos (si no existe)
Base.metadata.create_all(engine)
