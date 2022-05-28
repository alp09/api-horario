import os
import uvicorn
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from api.bbdd import bbdd
from api.config import SECRET_KEY
from api.routers import *


# App FastAPI
app = FastAPI()

# Permite probar OAuth2 sin necesidad de tener HTTPS
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# Añade los middleware
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# Registro de routers
app.include_router(router_login.router)
app.include_router(router_horario.router)
app.include_router(router_profesor.router)


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
