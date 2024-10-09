import bcrypt
from fastapi import FastAPI, Depends, HTTPException
from conexion import crear, get_db
from modelo import base, Emprendimiento
from sqlalchemy.orm import session
from shemas import Registrarse, Usuario, EliminarUsuario, RolCreate, EmprendimientoResponse, Login
from modelo import Usuario as Usuarios, Rol
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()
base.metadata.create_all(bind=crear)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint para crear un nuevo rol
@app.post("/roles", response_model=RolCreate)
async def crear_rol(rol: RolCreate, db: session = Depends(get_db)):
    # Verificar si el rol ya existe
    rol_existente = db.query(Rol).filter(rol.nombreRol == Rol.nombreRol).first()
    if rol_existente:
        raise HTTPException(status_code=400, detail="El rol ya existe")
    
    # Crear una nueva instancia del modelo `Rol`
    nuevo_rol = Rol(nombreRol=rol.nombreRol)
    
    # Agregar y guardar el nuevo rol en la base de datos
    db.add(nuevo_rol)
    db.commit()
    db.refresh(nuevo_rol)
    
    # Retornar la respuesta con los datos del nuevo rol
    return {
        "nombreRol": nuevo_rol.nombreRol
    }

@app.post("/registrate", response_model=EmprendimientoResponse)
async def registrarEmpresa(model: Registrarse, db: session = Depends(get_db)):
    # Verificar si el nombre del emprendimiento ya existe
    nombre_empresa = db.query(Emprendimiento).filter(Emprendimiento.nombreEmprendimiento == model.nombreEmprendimiento).first()
    if nombre_empresa:
        raise HTTPException(status_code=400, detail="El nombre del emprendimiento ya existe")
    
    # Verificar si el documento ya está registrado
    documento_existente = db.query(Emprendimiento).filter(Emprendimiento.documento == model.documento).first()
    if documento_existente:
        raise HTTPException(status_code=400, detail="El documento ya está registrado")
    
    # Encriptar la contraseña
    contraseña_encriptada = bcrypt.hashpw(model.contraseña.encode('utf-8'), bcrypt.gensalt())

    # Crear una nueva instancia del modelo `Emprendimiento`
    nuevo_emprendimiento = Emprendimiento(
        nombreEmprendimiento=model.nombreEmprendimiento,
        tipoEmprendimiento=model.tipoEmprendimiento,
        numeroEmpleados=model.numeroEmpleados,
        nombreRegistro=model.nombreRegistro,
        documento=model.documento,
        correoElectronico=model.correoElectronico,
        contraseña=contraseña_encriptada.decode('utf-8'),  # Almacenar la contraseña encriptada.
        rol=model.rol
    )

    # Agregar y guardar el nuevo emprendimiento en la base de datos
    db.add(nuevo_emprendimiento)
    db.commit()  # Confirmar los cambios
    db.refresh(nuevo_emprendimiento)  # Actualizar el objeto `nuevo_emprendimiento` con los datos de la base de datos

    # Retornar la respuesta con los datos registrados usando el nuevo modelo sin contraseña.
    return EmprendimientoResponse(
        nombreEmprendimiento=nuevo_emprendimiento.nombreEmprendimiento,
        tipoEmprendimiento=nuevo_emprendimiento.tipoEmprendimiento,
        numeroEmpleados=nuevo_emprendimiento.numeroEmpleados,
        nombreRegistro=nuevo_emprendimiento.nombreRegistro,
        documento=nuevo_emprendimiento.documento,
        correoElectronico=nuevo_emprendimiento.correoElectronico,
        rol=nuevo_emprendimiento.rol
    )

@app.post("/login")
async def login(user:Login,db:session=Depends(get_db)):
    db_user=db.query(Registrarse).filter(Registrarse == user.nombre_emprendimiento,
                                         Registrarse.rol == user.rol).first()
    if db_user is None:
        raise HTTPException(status_code=400, detail="Empremdimiento o tipo de usario incorrecto")
    if not bcrypt.checkpw(user.password.encode('utf-8'),db_user.password.encode('utf-8')):
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")
    
    return{
        "mensaje":"Inicio de sesión Ok",
        "nombreEmprendiminto":db_user.nombre_emprendimiento,
        "rol":db_user.rol
    }

@app.post("/usuario")
async def crear_usuario(usuario: Usuario, db: session = Depends(get_db)):
    # Buscar el rol por `rol_id`
    rol = db.query(Rol).filter(Rol.id == usuario.rol_id).first()
    if not rol:
        raise HTTPException(status_code=404, detail="El rol especificado no existe")
    # Encriptar la contraseña
    contraseña_encriptada = bcrypt.hashpw(usuario.contraseña.encode('utf-8'), bcrypt.gensalt())
    
    # Crear el nuevo usuario
    nuevo_usuario = Usuarios(
        nombre_usuario=usuario.nombre_usuario,
        documento=usuario.documento,
        correoElectronico=usuario.correoElectronico,
        contraseña=contraseña_encriptada.decode('utf-8'),
        rol_id=usuario.rol_id  # Asignar el rol
    )
    # Guardar en la base de datos
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return {"msg": "Usuario creado exitosamente"}



#endpoint para eliminar un usuario
@app.delete("/eliminarUsuario/")
async def eliminarUsuario(datos:  EliminarUsuario, db: session = Depends(get_db)):
    #buscar el usuario por su id
    usuario = db.query(Usuarios).filter(Usuarios.id == datos.usuario_id).first()
    #verificar si el ususraio existe
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    #verificar la contraseña
    if not bcrypt.checkpw(datos.contraseña.encode('utf-8'), usuario.contraseña.encode('utf-8')):
        raise HTTPException(status_code=403, detail="Contraseña incorrecta")
    
    # eliminar el usuario si la contraseña es valida
    db.delete(usuario)
    db.commit()  # confirmar los cambios en la base de datos

    return {"mensaje": f"Usuario con ID {datos.usuario_id} eliminado exitosamente"}



