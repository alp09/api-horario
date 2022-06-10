import os
import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from institutoapi.bbdd import bbdd
from institutoapi.config import SECRET_KEY
from institutoapi.routers import *


# App FastAPI
app = FastAPI()

# Permite probar OAuth2 sin necesidad de tener HTTPS
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# Añade los middleware
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
app.add_middleware(
	CORSMiddleware,
	allow_origins=["http://localhost:3000"],
	allow_credentials=True,
	allow_methods=["GET", "POST", "PUT", "DELETE"],
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


@app.on_event("startup")
def startup():
	# Inicializa la base de datos
	bbdd.inicializar_conexion()


@app.on_event("shutdown")
def shutdown():
	# Cierra la base de datos
	bbdd.cerrar_conexion()


if __name__ == "__main__":
	uvicorn.run(app, host="127.0.0.1", port=8000)