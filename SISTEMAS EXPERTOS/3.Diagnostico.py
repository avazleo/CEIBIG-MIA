import collections

# Solución de compatibilidad para Python 3.10+
if not hasattr(collections, 'Mapping'):
    import collections.abc
    collections.Mapping = collections.abc.Mapping
    collections.MutableMapping = collections.abc.MutableMapping
    collections.Sequence = collections.abc.Sequence
    collections.Iterable = collections.abc.Iterable

from experta import *

# 1. DEFINICIÓN DE HECHOS
class Paciente(Fact):
    """
    Datos del paciente:
    nombre, glucosa, edad, imc, historial_familiar (bool), sintomas (lista)
    """
    pass

class Diagnostico(KnowledgeEngine):

    # REGLA 1: Diagnóstico por Glucosa (Umbral > 126)
    @Rule(Paciente(nombre=MATCH.n, glucosa=P(lambda x: x > 126)))
    def glucosa_alta(self, n):
        print(f"ALERTA [{n}]: Nivel de glucosa en ayunas crítico (>126 mg/dL).")

    # REGLA 2: Diagnóstico por Factores de Riesgo Físicos (Edad e IMC)
    @Rule(
        Paciente(nombre=MATCH.n, edad=P(lambda x: x > 45), imc=P(lambda x: x > 25))
    )
    def riesgo_fisico(self, n):
        print(f"ALERTA [{n}]: Combinación de riesgo por edad (>45) e IMC (>25).")

    # REGLA 3: Diagnóstico por Historial Familiar
    @Rule(Paciente(nombre=MATCH.n, historial_familiar=True))
    def riesgo_hereditario(self, n):
        print(f"ALERTA [{n}]: El paciente cuenta con antecedentes familiares de diabetes.")

    # REGLA 4: Diagnóstico por Síntomas Específicos
    # Se activa si el paciente tiene al menos uno de los síntomas clave
    @Rule(
        Paciente(nombre=MATCH.n, sintomas=MATCH.s),
        TEST(lambda s: any(item in s for item in ["sed excesiva", "visión borrosa", "fatiga frecuente"]))
    )
    def presencia_sintomas(self, n, s):
        sintomas_detectados = [i for i in s if i in ["sed excesiva", "visión borrosa", "fatiga frecuente"]]
        print(f"ALERTA [{n}]: Presenta síntomas clínicos: {', '.join(sintomas_detectados)}.")

    # REGLA FINAL: Conclusión de Susceptibilidad
    # Esta regla se dispara si se cumple CUALQUIERA de las anteriores
    @Rule(
        OR(
            Paciente(glucosa=P(lambda x: x > 126)),
            AND(Paciente(edad=P(lambda x: x > 45)), Paciente(imc=P(lambda x: x > 25))),
            Paciente(historial_familiar=True),
            Paciente(sintomas=P(lambda s: any(i in s for i in ["sed excesiva", "visión borrosa", "fatiga frecuente"])))
        )
    )
    def diagnostico_final(self):
        print(">>> RESULTADO MÉDICO: El paciente es SUSCEPTIBLE de tener Diabetes Tipo 2. Se recomienda analítica completa.")

# 2. EJECUCIÓN DEL SISTEMA
engine = Diagnostico()
engine.reset()

# Caso de prueba: Paciente con varios factores de riesgo
engine.declare(Paciente(
    nombre="Juan Pérez",
    glucosa=130,
    edad=50,
    imc=28,
    historial_familiar=True,
    sintomas=["sed excesiva", "fatiga frecuente"]
))

print("--- INICIANDO DIAGNÓSTICO ---")
engine.run()