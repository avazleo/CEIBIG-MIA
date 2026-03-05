import collections
# Parche de compatibilidad para Python 3.10+
if not hasattr(collections, 'Mapping'):
    import collections.abc
    collections.Mapping = collections.abc.Mapping
    collections.MutableMapping = collections.abc.MutableMapping
    collections.Sequence = collections.abc.Sequence
    collections.Iterable = collections.abc.Iterable

from experta import *

class Solicitante(Fact):
    """Información sobre el candidato a la universidad."""
    pass

class SistemaAdmisiones(KnowledgeEngine):

    # REGLA 1: Admisión por Excelencia Académica y SAT
    # Requiere: Promedio > 85 Y SAT > 1200
    @Rule(
        Solicitante(promedio=P(lambda x: x > 85)),
        Solicitante(sat=P(lambda x: x > 1200))
    )
    def admision_estandar(self):
        print("Resultado: ADMITIDO (Razón: Excelencia académica y resultados SAT)")
        self.halt()

    # REGLA 2: Admisión por Perfil Integral (Extracurriculares)
    # Se dispara si tiene buen promedio y es activo fuera de clase
    @Rule(
        Solicitante(promedio=P(lambda x: x > 85)),
        Solicitante(extracurriculares=True)
    )
    def admision_integral(self):
        print("Resultado: ADMITIDO (Razón: Perfil integral y compromiso extracurricular)")
        self.halt()

    # REGLA 3: Admisión por Talento Excepcional (Excepciones)
    # No requiere nota mínima si el talento es sobresaliente
    @Rule(Solicitante(talento_excepcional=True))
    def admision_talento(self):
        print("Resultado: ADMITIDO (Razón: Talento excepcional o circunstancias únicas)")
        self.halt()

    # REGLA 4: Denegación por defecto
    # Se ejecuta si tras evaluar los hechos no se cumplen las condiciones de éxito
    # Usamos una prioridad (salience) baja para que sea la última en evaluarse
    @Rule(AS.s << Solicitante(), salience=-10)
    def denegacion_general(self, s):
        print("Resultado: NO ADMITIDO (Razón: No cumple con los criterios mínimos actuales)")

# --- Pruebas del Sistema ---

engine = SistemaAdmisiones()

# Caso A: Estudiante con talento especial (aunque no tenga SAT)
print("Evaluando Caso A...")
engine.reset()
engine.declare(Solicitante(promedio=70, sat=1000, talento_excepcional=True))
engine.run()

# Caso B: Estudiante con buen expediente pero sin extras
print("\nEvaluando Caso B...")
engine.reset()
engine.declare(Solicitante(promedio=90, sat=1300, talento_excepcional=False, extracurriculares=False))
engine.run()

# Caso C: Estudiante que no llega a los mínimos
print("\nEvaluando Caso C...")
engine.reset()
engine.declare(Solicitante(promedio=75, sat=1100, talento_excepcional=False, extracurriculares=True))
engine.run()