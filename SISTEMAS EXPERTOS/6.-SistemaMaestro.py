import collections
if not hasattr(collections, 'Mapping'):
    import collections.abc
    collections.Mapping = collections.abc.Mapping
    collections.MutableMapping = collections.abc.MutableMapping

import json
from experta import *

class Evidencia(Fact): pass

class Diagnostico(Fact): pass

class EvidenciaProcesada(Fact): pass  # Hecho para evitar bucles

class MotorProbabilistico(KnowledgeEngine):

    @Rule(
        # 1. Buscamos una evidencia
        Evidencia(sintoma=MATCH.s),
        # 2. Buscamos el diagnóstico de una enfermedad que tenga ese síntoma
        AS.f << Diagnostico(enfermedad=MATCH.e, probabilidad=MATCH.p),
        # 3. CRUCIAL: Solo disparamos si NO hemos procesado esta combinación antes
        NOT(EvidenciaProcesada(enfermedad=MATCH.e, sintoma=MATCH.s)),
        # 4. Comprobamos que el síntoma pertenece a la enfermedad
        TEST(lambda e, s: s in conocimiento_externo[e])
    )
    def incrementar_certeza(self, f, e, p, s):
        # Calculamos nueva probabilidad
        nueva_p = p + 0.2 * (1 - p)

        # Marcamos como procesado PRIMERO para evitar que el modify reactive esta misma combinación
        self.declare(EvidenciaProcesada(enfermedad=e, sintoma=s))

        # Modificamos el diagnóstico
        self.modify(f, probabilidad=round(nueva_p, 3))

        print(f"✨ Evidencia '{s}' procesada para {e}. Nueva probabilidad: {round(nueva_p, 3)}")

# 4. INTERFAZ DE INTEGRACIÓN
def sistema_maestro():
    # Cargar datos desde JSON
    with open('conocimiento.json') as f:
        datos = json.load(f)

    # Diccionario global para que el motor consulte los síntomas de cada enfermedad
    global conocimiento_externo
    conocimiento_externo = {enf['nombre']: enf['sintomas'] for enf in datos['enfermedades']}

    engine = MotorProbabilistico()

    while True:
        print("\n" + "=".upper() * 40)
        print("🚀 SISTEMA EXPERTO NIVEL MAESTRO")
        print("=".upper() * 40)
        print("1. Realizar Diagnóstico Probabilístico")
        print("2. Ver Base de Conocimiento (JSON)")
        print("3. Salir")

        op = input("\nSeleccione: ")

        if op == "1":
            engine.reset()  # Limpia la memoria interna

            # Guardamos las probabilidades base para comparar luego
            prob_bases = {enf['nombre']: enf['probabilidad_base'] for enf in datos['enfermedades']}

            # Declaramos los diagnósticos iniciales
            for enf in datos['enfermedades']:
                engine.declare(Diagnostico(enfermedad=enf['nombre'], probabilidad=enf['probabilidad_base']))

            print("\n--- INGRESO DE EVIDENCIAS ---")
            sintomas_input = input("Introduce síntomas: ").lower().split(",")

            for s in sintomas_input:
                engine.declare(Evidencia(sintoma=s.strip()))

            print("\n🧠 Procesando inferencias...")
            engine.run()

            print("\n📊 RESULTADOS DEL DIAGNÓSTICO:")
            coincidencias = 0
            for f in engine.facts.values():
                if isinstance(f, Diagnostico):
                    nombre_e = f['enfermedad']
                    prob_final = f['probabilidad']

                    # SOLO MOSTRAMOS si la probabilidad ha subido (hubo evidencia)
                    if prob_final > prob_bases[nombre_e]:
                        print(f"✅ {nombre_e}: {int(prob_final * 100)}% de certeza (Aumentó por evidencias)")
                        coincidencias += 1

            if coincidencias == 0:
                print("❌ No se encontraron coincidencias para los síntomas introducidos.")

        elif op == "2":
            print("\n📂 Datos cargados desde el archivo externo:")
            print(json.dumps(datos, indent=2))

        elif op == "3":
            break


if __name__ == "__main__":
    sistema_maestro()