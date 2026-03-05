import collections

# Solución de compatibilidad para Python 3.10+
if not hasattr(collections, 'Mapping'):
    import collections.abc
    collections.Mapping = collections.abc.Mapping
    collections.MutableMapping = collections.abc.MutableMapping
    collections.Sequence = collections.abc.Sequence
    collections.Iterable = collections.abc.Iterable

from experta import *


# 1. Definición de los Hechos (Atributos del Cliente)
class Cliente(Fact):
    """Información sobre el solicitante del crédito."""
    pass


# 2. Definición del Motor de Reglas
class SistemaConcesionCredito(KnowledgeEngine):

    # REGLA 1: Denegación por minoría de edad
    @Rule(Cliente(edad=P(lambda x: x < 18)))
    def menor_edad(self):
        print("Resultado: Crédito DENEGADO (Razón: Menor de edad)")
        self.halt()  # Detiene la ejecución si ya hay una causa de denegación

    # REGLA 2: Denegación por falta de nómina
    @Rule(Cliente(tiene_nomina=False))
    def sin_nomina(self):
        print("Resultado: Crédito DENEGADO (Razón: No dispone de nómina)")
        self.halt()

    # REGLA 3: Concesión por contrato indefinido (cumpliendo edad y nómina)
    @Rule(
        Cliente(edad=P(lambda x: x >= 18)),
        Cliente(tiene_nomina=True),
        Cliente(tipo_contrato="indefinido")
    )
    def contrato_indefinido(self):
        print("Resultado: Crédito CONCEDIDO (Razón: Contrato indefinido)")

    # REGLA 4: Concesión por contrato temporal de larga duración
    @Rule(
        Cliente(edad=P(lambda x: x >= 18)),
        Cliente(tiene_nomina=True),
        Cliente(tipo_contrato="temporal"),
        Cliente(duracion_contrato=MATCH.dur),
        Cliente(plazo_prestamo=MATCH.plazo),
        TEST(lambda dur, plazo: dur > plazo)
    )
    def contrato_temporal_valido(self, dur, plazo):
        print(f"R4 - Resultado: Crédito CONCEDIDO (Razón: Duración contrato {dur} > Plazo préstamo {plazo})")

    # REGLA 5: Denegación por contrato temporal insuficiente
    @Rule(
        Cliente(edad=P(lambda x: x >= 18)),
        Cliente(tiene_nomina=True),
        Cliente(tipo_contrato="temporal"),
        Cliente(duracion_contrato=MATCH.dur),
        Cliente(plazo_prestamo=MATCH.plazo),
        TEST(lambda dur, plazo: dur <= plazo)
    )
    def contrato_temporal_insuficiente(self):
        print("Resultado: Crédito DENEGADO (Razón: Duración de contrato insuficiente)")


# 3. Ejecución del Sistema
engine = SistemaConcesionCredito()
engine.reset()

# Ejemplo de un cliente para probar el sistema:
engine.declare(Cliente(
    edad=25,
    tiene_nomina=True,
    tipo_contrato="temporal",
    duracion_contrato=24,  # meses
    plazo_prestamo=12  # meses
))

engine.run()