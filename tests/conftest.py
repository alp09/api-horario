import pytest
from fastapi.testclient import TestClient

from institutoapi.main import app
from institutoapi.bbdd.modelos import Profesor
from institutoapi.middleware.auth import validar_profesor_logeado


@pytest.fixture(scope="session")
def cliente_no_autorizado():
	with TestClient(app) as test_client:
		yield test_client


@pytest.fixture(params=[True, False], ids=["admin", "estandar"])
def cliente_autorizado(cliente_no_autorizado, profesor_factory, request):

	def mock_validar_profesor_logeado() -> Profesor:
		return profesor_logeado

	profesor_logeado = profesor_factory(es_admin=request.param)
	app.dependency_overrides[validar_profesor_logeado] = mock_validar_profesor_logeado
	yield cliente_no_autorizado, profesor_logeado
	app.dependency_overrides.pop(validar_profesor_logeado)


@pytest.fixture(name="profesor_factory")
def crear_profesor():

	def _crear_profesor(codigo="TEST", nombre_completo="test", email="test@gmail.com", es_admin=True) -> Profesor:
		return Profesor(codigo=codigo, nombre_completo=nombre_completo, email=email, es_admin=es_admin)

	return _crear_profesor


@pytest.fixture(name="api_endpoint", params={"/asignaturas", "/aulas", "/grupos", "/profesores", "/horarios", "/reservas"})
def api_endpoint(request):
	return request.param
