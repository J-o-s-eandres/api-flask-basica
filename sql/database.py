from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging

# Configuración para SQLAlchemy
sql_logger = logging.getLogger('sqlalchemy.engine')
sql_logger.setLevel(logging.INFO)

#  guarda los mensajes en un archivo específico
file_handler = logging.FileHandler('logs/sql.log')
file_handler.setLevel(logging.INFO)

# formato para los mensajes de registro
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Agregar el handler al logger de SQLAlchemy
sql_logger.addHandler(file_handler)

engine = create_engine('sqlite:///users.db')  # 'echo=True' imprime las consultas SQL generadas

# sesión para interactuar con la base de datos
Session = sessionmaker(bind=engine)

session = Session()

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
