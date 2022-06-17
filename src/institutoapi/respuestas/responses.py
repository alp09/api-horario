from institutoapi.modelos import MensajeError


no_registrado = {
	401: {"model": MensajeError, "description": "El e-mail del usuario no está registrado"},
}

no_autorizado = {
	401: {"model": MensajeError, "description": "Es necesario iniciar sesión"},
	419: {"model": MensajeError, "description": "La sesión caducó. Inicia sesión de nuevo"},
}

permisos_insuficientes = {
	**no_autorizado,
	403: {"model": MensajeError, "description": "No tiene permisos suficientes"},
}

id_no_encontrado = {
	404: {"model": MensajeError, "description": "Recurso con el ID especificado no existe"},
}

sin_registros = {
	204: {"description": "La consulta no devolvió registros"},
}

error_integridad_bbdd = {
	409: {"model": MensajeError, "description": "Error de integridad en la BBDD"},
}

horario_invalido = {
	409: {"model": MensajeError, "description": "El horario indicado  no es compatible con el horario actual"},
}
