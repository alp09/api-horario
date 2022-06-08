from .esquemas_asignatura import Asignatura
from .esquemas_aula import Aula
from .esquemas_dia_semana import DiaSemana
from .esquemas_grupo import Grupo
from .esquemas_profesor import Profesor
from .esquemas_tramo import TramoHorario

# Se importan más tarde cuando los esquemas base ya estén cargados
from .esquemas_horario import HorarioIn, HorarioOut
from .esquemas_reserva import ReservaIn, ReservaOut
