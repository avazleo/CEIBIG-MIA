import collections
# Parche de compatibilidad para Python 3.10+
if not hasattr(collections, 'Mapping'):
    import collections.abc
    collections.Mapping = collections.abc.Mapping
    collections.MutableMapping = collections.abc.MutableMapping
    collections.Sequence = collections.abc.Sequence
    collections.Iterable = collections.abc.Iterable

from experta import *

# 1. Definición de Hechos (Hechos Simples)
class Perro(Fact): pass
class Gato(Fact): pass
class Grande(Fact): pass
class Pequeno(Fact): pass

class SistemaAnimales(KnowledgeEngine):

    # --- CONSULTA A y B: Animales por tamaño ---
    @Rule(OR(Perro(MATCH.a), Gato(MATCH.a)), Grande(MATCH.a))
    def animal_grande(self, a):
        print(f"Apartado A: {a} es un animal de tamaño GRANDE.")

    @Rule(OR(Perro(MATCH.b), Gato(MATCH.b)), Pequeno(MATCH.b))
    def animal_pequeno(self, b):
        print(f"Apartado B: {b} es un animal de tamaño PEQUEÑO.")

    # --- CONSULTA C: Listar todas las razas (Perros o Gatos) ---
    # Usamos un 'salience' alto para que esto sea lo primero que se muestre
    @Rule(OR(Perro(MATCH.raza), Gato(MATCH.raza)), salience=10)
    def listar_razas(self, raza):
        print(f"Apartado C (Raza registrada): {raza}")

    # --- CONSULTA D (Elección 1): Solo Perros Pequeños ---
    @Rule(Perro(MATCH.p), Pequeno(MATCH.p))
    def perro_pequeno(self, p):
        print(f"Apartado D1: {p} es específicamente un PERRO PEQUEÑO.")

    # --- CONSULTA D (Elección 2): Gatos Grandes ---
    @Rule(Gato(MATCH.g), Grande(MATCH.g))
    def gato_grande(self, g):
        print(f"Apartado D2: {g} es específicamente un GATO GRANDE.")

# --- EJECUCIÓN ---
engine = SistemaAnimales()
engine.reset()

# Declaramos la base de conocimientos (la "Base de Hechos" de Prolog)
engine.declare(Perro("rottweiler"), Perro("mastin"), Perro("bobtail"),
               Perro("chihuahua"), Perro("caniche"), Perro("pequines"))

engine.declare(Gato("siames"), Gato("ragdoll"), Gato("munchkin"), Gato("singapura"))

engine.declare(Grande("rottweiler"), Grande("mastin"), Grande("siames"),
               Grande("ragdoll"), Grande("bobtail"))

engine.declare(Pequeno("chihuahua"), Pequeno("singapura"), Pequeno("caniche"),
               Pequeno("pequines"), Pequeno("munchkin"))

engine.run()