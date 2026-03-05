import collections
if not hasattr(collections, 'Mapping'):
    import collections.abc
    collections.Mapping = collections.abc.Mapping
    collections.MutableMapping = collections.abc.MutableMapping

from experta import *


# 1. DEFINICIÓN DE HECHOS
class Progenitor(Fact): pass


class Hombre(Fact): pass


class Mujer(Fact): pass


class MotorGenealogicoCompleto(KnowledgeEngine):

    # REGLA: Definir Abuelos
    @Rule(
        Progenitor(progenitor=MATCH.abuelo, descendiente=MATCH.padre),
        Progenitor(progenitor=MATCH.padre, descendiente=MATCH.nieto)
    )
    def es_abuelo(self, abuelo, nieto):
        self.declare(Fact(parentesco="abuelo/a", de=abuelo, a=nieto))

    # REGLA: Definir Hermanos (Importante el TEST para no ser hermano de uno mismo)
    @Rule(
        Progenitor(progenitor=MATCH.p, descendiente=MATCH.h1),
        Progenitor(progenitor=MATCH.p, descendiente=MATCH.h2),
        TEST(lambda h1, h2: h1 != h2)
    )
    def son_hermanos(self, h1, h2):
        self.declare(Fact(parentesco="hermano/a", de=h1, a=h2))

    # REGLA: Definir Tíos
    @Rule(
        Fact(parentesco="hermano/a", de=MATCH.tio, a=MATCH.progenitor),
        Progenitor(progenitor=MATCH.progenitor, descendiente=MATCH.sobrino)
    )
    def es_tio(self, tio, sobrino):
        self.declare(Fact(parentesco="tio/a", de=tio, a=sobrino))

    # REGLA: Definir Primos (Hijos de hermanos)
    @Rule(
        Fact(parentesco="hermano/a", de=MATCH.p1, a=MATCH.p2),
        Progenitor(progenitor=MATCH.p1, descendiente=MATCH.hijo1),
        Progenitor(progenitor=MATCH.p2, descendiente=MATCH.hijo2)
    )
    def son_primos(self, hijo1, hijo2):
        self.declare(Fact(parentesco="primo/a", de=hijo1, a=hijo2))


# 2. INTERFAZ DINÁMICA CON OPCIÓN DE PRIMOS
def arbol_interactivo():
    engine = MotorGenealogicoCompleto()

    # Base de datos persistente
    bd_hechos = [
        Progenitor(progenitor="Antonio", descendiente="Juan"),
        Progenitor(progenitor="Antonio", descendiente="Maria"),
        Progenitor(progenitor="Ana", descendiente="Juan"),
        Progenitor(progenitor="Juan", descendiente="Pedro"),
        Progenitor(progenitor="Maria", descendiente="Laura"),
        Hombre("Antonio"), Hombre("Juan"), Hombre("Pedro"),
        Mujer("Ana"), Mujer("Maria"), Mujer("Laura")
    ]

    while True:
        engine.reset()
        for h in bd_hechos:
            engine.declare(h)
        engine.run()

        print("\n" + "—" * 45)
        print("🌳 SISTEMA GENEALÓGICO EXPERTO v4.0")
        print("—" * 45)
        print("1. Consultar Abuelos")
        print("2. Consultar Hermanos")
        print("3. Consultar Tíos")
        print("4. Consultar Primos")
        print("5. Ver INFORME de parentescos (IA)")
        print("6. ➕ AGREGAR NUEVO MIEMBRO")
        print("7. Salir")

        opcion = input("\nSeleccione opción: ")

        if opcion == "1":
            nieto = input("Nombre del nieto/a: ").capitalize()
            encontrados = [f['de'] for f in engine.facts.values() if
                           f.get('parentesco') == "abuelo/a" and f['a'] == nieto]
            print(f"-> Abuelos/as: {', '.join(set(encontrados))}" if encontrados else "No encontrados.")

        elif opcion == "2":
            persona = input("Nombre: ").capitalize()
            hermanos = {f['a'] for f in engine.facts.values() if
                        f.get('parentesco') == "hermano/a" and f['de'] == persona}
            print(f"-> Hermanos/as: {', '.join(hermanos)}" if hermanos else "No tiene hermanos registrados.")

        elif opcion == "3":
            sobrino = input("Nombre del sobrino/a: ").capitalize()
            tios = {f['de'] for f in engine.facts.values() if f.get('parentesco') == "tio/a" and f['a'] == sobrino}
            print(f"-> Tíos/as: {', '.join(tios)}" if tios else "No encontrados.")

        elif opcion == "4":
            persona = input("¿De quién quieres buscar los primos/as?: ").capitalize()
            primos = {f['a'] for f in engine.facts.values() if f.get('parentesco') == "primo/a" and f['de'] == persona}
            print(f"-> Primos/as de {persona}: {', '.join(primos)}" if primos else "No tiene primos registrados.")

        elif opcion == "5":
            print("\n--- INFORME DE INFERENCIAS ---")
            for f in engine.facts.values():
                if f.get('parentesco'):
                    print(f"DEDUCCIÓN: {f['de']} es {f['parentesco']} de {f['a']}")

        elif opcion == "6":
            nombre = input("Nombre del nuevo miembro: ").capitalize()
            padre = input(f"¿Quién es el progenitor de {nombre}?: ").capitalize()
            sexo = input("Sexo (H/M): ").upper()
            bd_hechos.append(Progenitor(progenitor=padre, descendiente=nombre))
            if sexo == "H":
                bd_hechos.append(Hombre(nombre))
            else:
                bd_hechos.append(Mujer(nombre))
            print(f"✅ {nombre} añadido. Procesando nuevas relaciones...")

        elif opcion == "7":
            break


arbol_interactivo()