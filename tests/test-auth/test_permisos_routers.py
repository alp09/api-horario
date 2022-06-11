import pytest
from fastapi import status
from fastapi.testclient import TestClient


def test_cliente_no_autorizado_no_puede_acceder(cliente_no_autorizado: TestClient, api_endpoint: str):
	response = cliente_no_autorizado.get(api_endpoint)
	assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_cliente_autorizado_puede_acceder(cliente_autorizado, api_endpoint: str):
	cliente_api, _ = cliente_autorizado
	response = cliente_api.get(api_endpoint)
	assert response.status_code != status.HTTP_401_UNAUTHORIZED


def test_validar_permisos_cliente_autorizado(cliente_autorizado, api_endpoint: str):
	if api_endpoint == "/reservas":
		pytest.skip("No es necesario ser administrador para usar el endpoint /reservas")

	cliente_api, profesor_logeado = cliente_autorizado
	response = cliente_api.post(api_endpoint)
	assert (response.status_code != status.HTTP_403_FORBIDDEN) == profesor_logeado.es_admin
