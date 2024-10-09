from pydantic import BaseModel

class Registrarse(BaseModel):
    nombreEmprendimiento: str
    tipoEmprendimiento: str
    numeroEmpleados: int
    nombreRegistro: str
    documento: str
    correoElectronico: str
    contraseña: str
    rol: str

class EmprendimientoResponse(BaseModel):
    nombreEmprendimiento: str
    tipoEmprendimiento: str
    numeroEmpleados: int
    nombreRegistro: str
    documento: str
    correoElectronico: str
    rol: str

class RolCreate(BaseModel):
    nombreRol: str

class Usuario(BaseModel):
    documento: int
    nombre_usuario: str
    rolUsuario: str  # Aquí debe estar el campo rolUsuario
    password: str

class EliminarUsuario(BaseModel):
    usuario_id: int
    contraseña: str

class Login(BaseModel):
   nombre_emprendimiento: str
   rol:str
   password:str 