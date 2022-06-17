import os
import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from institutoapi.bbdd import bbdd
from institutoapi.config import ApiConfig as Cfg
from institutoapi.routers import *


# App FastAPI
app = FastAPI(
	title="API reservas",
	description="""
	
API para la gestión de horarios y reservas de aulas del instituto.
	
## Features

- ### Gestión de horario y reservas

	La API proveé rutas para manipular los datos de asignaturas, aulas, grupos, profesores, horarios y reservas. Todas las rutas están protegidas bajo autorización por tokens.

- ### Autenticación mediante Google API

    La API es totalmente segura, ya que en ningún momento tiene acceso a información sensible. Esto se debe a que la autenticación se realiza en los servidores seguros de Google. La única información a la que se tiene acceso es el e-mail, con el que se verifica la identidad del profesor que intenta usar la API. 

- ### Autorización con tokens JWT

    Una vez el profesor se identifica, se le concede un token JWT firmado por el servidor con el que podrá demostrar su identidad en las futuras peticiones que realice.
    
    Este token también se usa para validar los roles del profesor cuando intenta acceder a rutas restringidas. 
	
	""",
	version="1.0.0",
	contact={
		"name": "Abel López Parrado",
		"email": "abellp13@gmail.com",
	},
)

# Permite probar OAuth2 sin necesidad de tener HTTPS
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# Añade los middleware
app.add_middleware(SessionMiddleware, secret_key=Cfg.secret_key)
app.add_middleware(
	CORSMiddleware,
	allow_origins=Cfg.origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

# Registro de routers
app.include_router(router_asignatura.router)
app.include_router(router_aula.router)
app.include_router(router_grupo.router)
app.include_router(router_horario.router)
app.include_router(router_login.router)
app.include_router(router_profesor.router)
app.include_router(router_reserva.router)

if __name__ == "__main__":

	@app.on_event("startup")
	def startup():
		# Inicializa la base de datos
		bbdd.inicializar_conexion(url=Cfg.db_url)

	@app.on_event("shutdown")
	def shutdown():
		# Cierra la base de datos
		bbdd.finalizar_conexion()

	uvicorn.run(app, host=Cfg.api_host, port=Cfg.api_port)
