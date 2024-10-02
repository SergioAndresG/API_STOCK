#Se usa para la configuaracion de las bases de datos 
from sqlalchemy import create_engine
#Se usa para crar una clase base en donde se definiran los modelos de dartos
from sqlalchemy.ext.declarative import declarative_base
#Se usa para crear una clase de sesion que luego se usa para instanciar, sesiones
from sqlalchemy.orm import sessionmaker


#Definimos una url con la cual vamos a ingresar a la base de datos
URL_DB = "mysql+mysqlconnector://root:larata420@localhost:3306/stock"
#Se crea el motor de la base de datos, con la url utilizada
crear = create_engine(URL_DB)
#Defi
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=crear)
base = declarative_base()

def get_db():
    cnn = SessionLocal()
    try:
        yield cnn
    finally:
        cnn.close()



