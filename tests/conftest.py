import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from sqlmodel.pool import StaticPool

from institutoapi.main import app
from institutoapi.bbdd.bbdd import get_sesion
from institutoapi.modelos import Profesor
from institutoapi.middleware import auth_middleware as auth


@pytest.fixture(name="db_engine", scope="session")
def engine_base_de_datos():
	engine = create_engine(url="sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
	SQLModel.metadata.create_all(bind=engine)
	yield engine


@pytest.fixture(scope="session")
def sesion(db_engine):
	with Session(bind=db_engine) as sesion:
		yield sesion


@pytest.fixture(scope="session")
def cliente_no_autorizado(sesion):

	def mock_sesion_db():
		return sesion

	with TestClient(app) as test_client:
		app.dependency_overrides[get_sesion] = mock_sesion_db
		yield test_client
		app.dependency_overrides.pop(get_sesion)


@pytest.fixture(params=[True, False], ids=["admin", "estandar"])
def cliente_autorizado(cliente_no_autorizado, profesor_factory, request):

	def mock_validar_profesor_logeado() -> Profesor:
		return profesor_logeado

	profesor_logeado = profesor_factory(es_admin=request.param)
	app.dependency_overrides[auth.validar_profesor_logeado] = mock_validar_profesor_logeado
	yield cliente_no_autorizado, profesor_logeado
	app.dependency_overrides.pop(auth.validar_profesor_logeado)


@pytest.fixture(name="profesor_factory")
def crear_profesor():

	def _crear_profesor(codigo="TEST", nombre_completo="test", email="test@gmail.com", es_admin=True) -> Profesor:
		return Profesor(codigo=codigo, nombre_completo=nombre_completo, email=email, es_admin=es_admin)

	return _crear_profesor


@pytest.fixture(name="api_endpoint", params={"/asignaturas", "/aulas", "/grupos", "/profesores", "/horarios", "/reservas"})
def api_endpoint(request):
	return request.param
