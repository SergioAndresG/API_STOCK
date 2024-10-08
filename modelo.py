from sqlalchemy import String, Integer, Column, ForeignKey
from conexion import base
from sqlalchemy.orm import relationship

# Tabla de Registro de Emprendimientos
from sqlalchemy import String, Integer, Column
from sqlalchemy.ext.declarative import declarative_base


class Emprendimiento(base):
    __tablename__ = "Registrate"
    documento = Column(String(30), primary_key=True, autoincrement=False)
    # Nombre del emprendimiento, no debe ser nulo
    nombreEmprendimiento = Column(String(50), nullable=False, index=True)
    # Tipo de emprendimiento, no debe ser nulo
    tipoEmprendimiento = Column(String(50), nullable=False)
    # Número de empleados, debe ser un Integer normal
    numeroEmpleados = Column(Integer, nullable=True)
    # Nombre del registro único
    nombreRegistro = Column(String(50), unique=True, nullable=False)
    # Correo electrónico, único para evitar duplicados
    correoElectronico = Column(String(50), unique=True, nullable=False)
    # Contraseña, no debe ser única ni indexada
    contraseña = Column(String(150), nullable=False)
    # Roles
    rol = Column(String(30), nullable=False)




class Rol(base):
    __tablename__ = "Roles"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombreRol = Column(String(50), unique=True, nullable=False)  # Roles como "Administrador", "Jefe", "Empleado"

class Usuario(base):
    __tablename__ = "Usuarios"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_usuario = Column(String(50), nullable=False, unique=True)
    documento = Column(String(25), unique=True, nullable=False)  # Documento de identidad único
    correoElectronico = Column(String(50), unique=True, nullable=False)
    contraseña = Column(String(100), nullable=False)
    # Relación con la tabla de roles
    rol_id = Column(Integer, ForeignKey('Roles.id'), nullable=False)  # El rol de este usuario
    rol = relationship("Rol")
    # Nueva columna para enlazar con la tabla `Emprendimiento`
    nombreEmprendimiento = Column(String(50), ForeignKey('Registrate.nombreEmprendimiento'), nullable=False)
    # Relación con la tabla `Emprendimiento`
    emprendimiento = relationship("Emprendimiento", backref="usuarios")


class Producto(base):
    __tablename__ = "Productos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombreProducto = Column(String(50), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio = Column(Integer, nullable=False)
    # El usuario que creó o gestionó el producto (probablemente un jefe o administrador)
    gestionado_por = Column(Integer, ForeignKey('Usuarios.id'), nullable=False)
    usuario = relationship("Usuario")

class Permiso(base):
    __tablename__ = "Permisos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    descripcion = Column(String(100), nullable=False)
    rol_id = Column(Integer, ForeignKey('Roles.id'), nullable=False)
    rol = relationship("Rol") 







