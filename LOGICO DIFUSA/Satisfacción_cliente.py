import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

t_respuesta = ctrl.Antecedent(np.arange(0, 31, 1), 't_respuesta')
calidad_prod = ctrl.Antecedent(np.arange(0, 11, 1), 'calidad_prod')
satisfaccion = ctrl.Consequent(np.arange(0, 101, 1), 'satisfaccion')

t_respuesta['rapido'] = fuzz.trimf(t_respuesta.universe, [0, 0, 10])
t_respuesta['moderado'] = fuzz.trimf(t_respuesta.universe, [5, 10, 20])
t_respuesta['lento'] = fuzz.trimf(t_respuesta.universe, [15, 25, 30])

calidad_prod['baja'] = fuzz.trimf(calidad_prod.universe, [0, 0, 5])
calidad_prod['media'] = fuzz.trimf(calidad_prod.universe, [3, 5, 7])
calidad_prod['alta'] = fuzz.trimf(calidad_prod.universe, [5, 10, 10])

satisfaccion['insatisfecho'] = fuzz.trimf(satisfaccion.universe, [0, 0, 40])
satisfaccion['satisfecho'] = fuzz.trimf(satisfaccion.universe, [30, 50, 70])
satisfaccion['muy_satisfecho'] = fuzz.trimf(satisfaccion.universe, [60, 100, 100])

rule1 = ctrl.Rule(t_respuesta['rapido'] & calidad_prod['alta'], satisfaccion['muy_satisfecho'])
rule2 = ctrl.Rule(t_respuesta['moderado'] & calidad_prod['media'], satisfaccion['satisfecho'])
rule3 = ctrl.Rule(t_respuesta['lento'] & calidad_prod['baja'], satisfaccion['insatisfecho'])


sistema = ctrl.ControlSystem([rule1, rule2, rule3])
simulacion = ctrl.ControlSystemSimulation(sistema)

# Parte del problema

simulacion.input['t_respuesta'] = 15
simulacion.input['calidad_prod'] = 6

simulacion.compute()
resultado = simulacion.output['satisfaccion']

# Grado de pertenencia del valor defuzzificado
insatisfecho = fuzz.interp_membership(
    satisfaccion.universe, satisfaccion['insatisfecho'].mf, resultado)

satisfecho = fuzz.interp_membership(
    satisfaccion.universe, satisfaccion['satisfecho'].mf, resultado)

m_satisfecho = fuzz.interp_membership(
    satisfaccion.universe, satisfaccion['muy_satisfecho'].mf, resultado)

print(f"Resultado numérico: {resultado:.2f}")
print(f"Pertenencia a INSATISFECHO: {insatisfecho:.2f}")
print(f"Pertenencia a SATISFECHO: {satisfecho:.2f}")
print(f"Pertenencia a MUY SATISFECHO: {m_satisfecho:.2f}")