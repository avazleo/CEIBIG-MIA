# 1. Instalación y parche de compatibilidad
import collections
if not hasattr(collections, 'Mapping'):
    import collections.abc
    collections.Mapping = collections.abc.Mapping
    collections.MutableMapping = collections.abc.MutableMapping

from experta import *

# 2. DEFINICIÓN DE HECHOS (Basado en Figura 5.11)
class Hombre(Fact):
    """Equivalente a hombre(nombre)."""
    pass

class Mujer(Fact):
    """Equivalente a mujer(nombre)."""
    pass

class Progenitor(Fact):
    """Equivalente a progenitor(padre_madre, hijo_hija)."""
    pass

# 3. MOTOR DE INFERENCIA (Reglas de la Figura 5.14)
class ArbolGenealogico(KnowledgeEngine):

    # --- REGLAS DE PARENTESCO BÁSICAS ---

    @Rule(Hombre(MATCH.p), Progenitor(progenitor=MATCH.p, descendiente=MATCH.h))
    def es_padre(self, p, h):
        print(f"[LOG] {p} es PADRE de {h}")

    @Rule(Mujer(MATCH.m), Progenitor(progenitor=MATCH.m, descendiente=MATCH.h))
    def es_madre(self, m, h):
        print(f"[LOG] {m} es MADRE de {h}")

    # --- RESOLUCIÓN DE ACTIVIDADES ---

    # Actividad A: Abuelos de JuanIII
    @Rule(
        Progenitor(progenitor=MATCH.abuelo, descendiente=MATCH.padre_madre),
        Progenitor(progenitor=MATCH.padre_madre, descendiente="juanIII")
    )
    def actividad_a(self, abuelo):
        print(f"APARTADO A: {abuelo} es ABUELO/A de juanIII")

    # Actividad B y D: Hermanos de CarmenII / FernandoII
    @Rule(
        Progenitor(progenitor=MATCH.p, descendiente=MATCH.h1),
        Progenitor(progenitor=MATCH.p, descendiente=MATCH.h2),
        TEST(lambda h1, h2: h1 != h2)
    )
    def actividad_b_d(self, h1, h2):
        if h1 == "fernandoII" and h2 == "carmenII":
            print("APARTADO B: Confirmado, fernandoII y carmenII son hermanos.")
        if h2 == "carmenII":
            print(f"APARTADO D: {h1} es hermano/a de carmenII")

    # Actividad C: Determinar sexo para saber si es hermano o hermana
    @Rule(
        Progenitor(progenitor=MATCH.p, descendiente=MATCH.sujeto),
        Progenitor(progenitor=MATCH.p, descendiente=MATCH.pariente),
        Hombre(MATCH.sujeto),
        TEST(lambda sujeto, pariente: sujeto != pariente)
    )
    def actividad_c(self, sujeto, pariente):
        # Esta regla identifica específicamente cuando el hermano es varón
        if sujeto == "fernandoII" and pariente == "carmenII":
            print(f"APARTADO C: {sujeto} es HOMBRE, por tanto es HERMANO de {pariente}")

# 4. EJECUCIÓN CON DATOS REALES (Figuras 5.11 y 5.12)
engine = ArbolGenealogico()
engine.reset()

# Declaración de Sexos (Figura 5.11)
engine.declare(Hombre("fernandoI"), Mujer("carmenI"), Hombre("leandroI"), Mujer("mercedesi"))
engine.declare(Hombre("fernandoII"), Mujer("palomaII"), Mujer("carmenII"), Mujer("victoriaII"), Hombre("miguelII"))
engine.declare(Hombre("juanIII"), Hombre("fernandoIII"), Mujer("isabelIII"))

# Relaciones de Progenitura (Figura 5.12)
# Hijos de FernandoI y CarmenI
for hijo in ["fernandoII", "palomaII", "carmenII", "victoriaII"]:
    engine.declare(Progenitor(progenitor="fernandoI", descendiente=hijo))
    engine.declare(Progenitor(progenitor="carmenI", descendiente=hijo))

# Padres de JuanIII
engine.declare(Progenitor(progenitor="victoriaII", descendiente="juanIII"))
engine.declare(Progenitor(progenitor="miguelII", descendiente="juanIII"))

# Padres de MiguelII
engine.declare(Progenitor(progenitor="leandroI", descendiente="miguelII"))
engine.declare(Progenitor(progenitor="mercedesi", descendiente="miguelII"))

# DISPARAR EL MOTOR
print("--- RESULTADOS DEL SISTEMA EXPERTO ---")
engine.run()