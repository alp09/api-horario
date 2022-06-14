import os
import uvicorn
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from institutoapi.bbdd import bbdd
from institutoapi.config import ApiConfig as Cfg
from institutoapi.routers import *


# App FastAPI
app = FastAPI()

# Permite probar OAuth2 sin necesidad de tener HTTPS
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# Añade los middleware
app.add_middleware(SessionMiddleware, secret_key=Cfg.secret_key)

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
		bbdd.inicializar_conexion(
			username=Cfg.db_username,
			password=Cfg.db_password,
			host=Cfg.db_host,
			port=Cfg.db_port,
			database=Cfg.db_database,
			echo=True,
		)

	@app.on_event("shutdown")
	def shutdown():
		# Cierra la base de datos
		bbdd.finalizar_conexion()

	uvicorn.run(app, host="127.0.0.1", port=8000)
