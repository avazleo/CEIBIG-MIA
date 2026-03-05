import collections
if not hasattr(collections, 'Mapping'):
    import collections.abc
    collections.Mapping = collections.abc.Mapping
    collections.MutableMapping = collections.abc.MutableMapping

from experta import *


# 1. DEFINICIÓN DE HECHOS
class Padece(Fact): pass


class SintomaDe(Fact): pass


class Suprime(Fact): pass


class MotorMedicoAvanzado(KnowledgeEngine):

    @Rule(
        SintomaDe(sintoma=MATCH.s, enfermedad=MATCH.e),
        Suprime(farmaco=MATCH.f, sintoma=MATCH.s),
        salience=10
    )
    def inferir_alivio(self, f, e):
        self.declare(Fact(alivia=(f, e)))


# 2. INTERFAZ Y LÓGICA DE CONTROL
def asistente_medico():
    engine = MotorMedicoAvanzado()
    engine.reset()

    # --- BASE DE CONOCIMIENTO ---
    engine.declare(
        SintomaDe(sintoma="fiebre", enfermedad="gripe"),
        SintomaDe(sintoma="tos", enfermedad="gripe"),
        SintomaDe(sintoma="cansancio", enfermedad="gripe"),
        SintomaDe(sintoma="cansancio", enfermedad="hepatitis"),
        SintomaDe(sintoma="ictericia", enfermedad="hepatitis"),
        SintomaDe(sintoma="diarrea", enfermedad="intoxicacion"),
        SintomaDe(sintoma="nauseas", enfermedad="intoxicacion"),
        SintomaDe(sintoma="dolor de cabeza", enfermedad="migraña"),
        SintomaDe(sintoma="sensibilidad luz", enfermedad="migraña"),

        Suprime(farmaco="Aspirina", sintoma="fiebre"),
        Suprime(farmaco="Lomotil", sintoma="diarrea"),
        Suprime(farmaco="Paracetamol", sintoma="dolor de cabeza"),
        Suprime(farmaco="Reposo", sintoma="ictericia"),

        Padece(persona="Pedro", enfermedad="gripe"),
        Padece(persona="Pedro", enfermedad="hepatitis"),
        Padece(persona="Ana", enfermedad="migraña"),
        Padece(persona="Carlos", enfermedad="intoxicacion"),
        Padece(persona="Maria", enfermedad="gripe")
    )

    engine.run()

    while True:
        print("\n" + "—" * 45)
        print("🩺 SISTEMA MÉDICO INTERACTIVO")
        print("—" * 45)
        print("1. Consultar fármaco para enfermedad")
        print("2. Ver receta de paciente")
        print("3. Buscar pacientes por SÍNTOMA")
        print("4. Diagnóstico por síntomas (Triaje)")
        print("5. Salir")

        opcion = input("\nSeleccione: ")

        if opcion == "1":
            enf = input("Enfermedad: ").lower()
            encontrado = False
            for f in engine.facts.values():
                if f.get('alivia') and f['alivia'][1] == enf:
                    print(f"✅ Recomendado: {f['alivia'][0]}")
                    encontrado = True
            if not encontrado: print("No hay fármaco específico.")

        elif opcion == "2":
            paciente = input("Nombre del paciente: ").capitalize()
            encontrado = False
            for f in engine.facts.values():
                if isinstance(f, Padece) and f['persona'] == paciente:
                    encontrado = True
                    e = f['enfermedad']
                    print(f"- Diagnóstico: {e.upper()}")
                    # Buscar alivio para esa enfermedad
                    for f2 in engine.facts.values():
                        if f2.get('alivia') and f2['alivia'][1] == e:
                            print(f"  💊 Receta: {f2['alivia'][0]}")
            if not encontrado: print("Paciente no registrado.")

        elif opcion == "3":
            busqueda = input("Introduce el síntoma (fiebre/cansancio/diarrea/etc): ").lower()
            print(f"\nResultados para '{busqueda}':")

            # Paso 1: Ver qué enfermedades tienen ese síntoma
            enfermedades_con_sintoma = [f['enfermedad'] for f in engine.facts.values()
                                        if isinstance(f, SintomaDe) and f['sintoma'] == busqueda]

            # Paso 2: Ver qué personas tienen esas enfermedades
            pacientes_afectados = []
            for f in engine.facts.values():
                if isinstance(f, Padece) and f['enfermedad'] in enfermedades_con_sintoma:
                    pacientes_afectados.append(f['persona'])

            if pacientes_afectados:
                for p in set(pacientes_afectados):  # set() para no repetir si tiene 2 enfermedades con mismo síntoma
                    print(f"-> El paciente {p} presenta {busqueda}")
            else:
                print("No hay registros de pacientes con ese síntoma.")

        elif opcion == "4":
            s1 = input("Síntoma 1: ").lower()
            s2 = input("Síntoma 2: ").lower()

            # Buscar enfermedades que coincidan
            e1 = {f['enfermedad'] for f in engine.facts.values() if isinstance(f, SintomaDe) and f['sintoma'] == s1}
            e2 = {f['enfermedad'] for f in engine.facts.values() if isinstance(f, SintomaDe) and f['sintoma'] == s2}
            coincidencias = e1.intersection(e2)

            if coincidencias:
                print(f"🔍 Diagnóstico posible: {', '.join(coincidencias)}")
            else:
                print("🚨 ALERTA: Cuadro desconocido. ¡Acuda a URGENCIAS!")

        elif opcion == "5":
            break


asistente_medico()