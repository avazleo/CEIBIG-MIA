import collections
if not hasattr(collections, 'Mapping'):
    import collections.abc
    collections.Mapping = collections.abc.Mapping
    collections.MutableMapping = collections.abc.MutableMapping

import json
from experta import *


# 1. DEFINICIÓN DE HECHOS
class Evidencia(Fact): pass  # Síntoma que el usuario introduce

class Diagnostico(Fact): pass  # Resultado acumulativo

class RelacionSintoma(Fact): pass  # CONOCIMIENTO: "La enfermedad X tiene el síntoma Y"

class EvidenciaProcesada(Fact): pass  # Control de bucles

class MotorPuro(KnowledgeEngine):

    # REGLA MAESTRA: Ahora el motor empareja TRES hechos simultáneamente
    @Rule(
        # A. Buscamos un síntoma introducido
        Evidencia(sintoma=MATCH.s),

        # B. Buscamos en el conocimiento si ese síntoma pertenece a una enfermedad
        # ¡Aquí el motor hace el trabajo que antes hacía el TEST!
        RelacionSintoma(enfermedad=MATCH.e, sintoma=MATCH.s),

        # C. Buscamos el diagnóstico actual de esa enfermedad
        AS.f << Diagnostico(enfermedad=MATCH.e, probabilidad=MATCH.p),

        # D. Filtro de seguridad para no repetir
        NOT(EvidenciaProcesada(enfermedad=MATCH.e, sintoma=MATCH.s))
    )
    def incrementar_certeza(self, f, e, p, s):
        nueva_p = p + 0.2 * (1 - p)
        self.declare(EvidenciaProcesada(enfermedad=e, sintoma=s))
        self.modify(f, probabilidad=round(nueva_p, 3))
        print(f"✨ Lógica Pura: '{s}' validado para {e}. Probabilidad sube a: {round(nueva_p, 3)}")


# 2. INTERFAZ Y CARGA DE DATOS
def sistema_facts():
    # Cargar JSON
    with open('conocimiento.json') as f:
        datos = json.load(f)

    engine = MotorPuro()

    while True:
        print("\n" + "=".upper() * 40)
        print("🏛️ SISTEMA EXPERTO: LÓGICA DE HECHOS")
        print("=".upper() * 40)
        print("1. Realizar Diagnóstico")
        print("2. Salir")

        op = input("\nSeleccione: ")

        if op == "1":
            engine.reset()

            # --- CARGA DEL CONOCIMIENTO ESTRUCTURAL ---
            # Transformamos el JSON en Hechos antes de arrancar
            for enf in datos['enfermedades']:
                # 1. Creamos la base del diagnóstico
                engine.declare(Diagnostico(enfermedad=enf['nombre'],
                                           probabilidad=enf['probabilidad_base']))
                # 2. Creamos un hecho por cada síntoma (El "Manual Médico")
                for s in enf['sintomas']:
                    engine.declare(RelacionSintoma(enfermedad=enf['nombre'], sintoma=s))

            sintomas_input = input("\nIntroduce síntomas (fiebre, tos): ").lower().split(",")
            for s in sintomas_input:
                engine.declare(Evidencia(sintoma=s.strip()))

            print("\n🧠 El algoritmo Rete está emparejando los hechos...")
            engine.run()

            # (Opcional: Filtrar resultados como en el ejemplo anterior)
            print("\n📊 RESULTADOS FINALES:")
            for f in engine.facts.values():
                if isinstance(f, Diagnostico):
                    print(f"-> {f['enfermedad']}: {int(f['probabilidad'] * 100)}% certeza")

        elif op == "2":
            break


sistema_facts()