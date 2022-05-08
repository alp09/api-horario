from sqlalchemy import Column, ForeignKey, Integer, String

from ..bbdd import Base


class Horario(Base):
	__tablename__ = "horario"

	# Columnas
	id					= Column(Integer(), primary_key=True)
	id_dia				= Column(Integer(), ForeignKey("dia_semana.id"))
	id_tramo			= Column(Integer(), ForeignKey("tramo_horario.id"))
	codigo_asignatura	= Column(String(20), ForeignKey("asignatura.codigo"))
	codigo_profesor		= Column(String(20), ForeignKey("profesor.codigo"))
	codigo_aula			= Column(String(20), ForeignKey("aula.codigo"), nullable=True)
	codigo_grupo		= Column(String(20), ForeignKey("grupo.codigo"), nullable=True)
