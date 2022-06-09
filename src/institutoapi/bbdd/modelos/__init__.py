from .modelo_asignatura import Asignatura
from .modelo_aula import Aula
from .modelo_dia_semana import DiaSemana
from .modelo_grupo import Grupo
from .modelo_profesor import Profesor
from .modelo_tramo_horario import TramoHorario

# Se importan al final cuando los modelos base estén cargados
from .modelo_horario import Horario, HorarioRequest, HorarioResponse
from .modelo_reserva import Reserva, ReservaRequest, ReservaResponse
