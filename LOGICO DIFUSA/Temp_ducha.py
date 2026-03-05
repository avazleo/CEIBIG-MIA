import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Universos
temp_agua = ctrl.Antecedent(np.arange(0, 61, 1), 'temp_agua')
tiempo = ctrl.Antecedent(np.arange(0, 31, 1), 'tiempo')
salida = ctrl.Consequent(np.arange(0, 101, 1), 'salida')

temp_agua['fria'] = fuzz.trimf(temp_agua.universe, [0, 0, 20])
temp_agua['templada'] = fuzz.trimf(temp_agua.universe, [15, 27, 40])
temp_agua['caliente'] = fuzz.trimf(temp_agua.universe, [30, 60, 60])

tiempo['corto'] = fuzz.trimf(tiempo.universe, [0, 0, 10])
tiempo['medio'] = fuzz.trimf(tiempo.universe, [5, 12, 20])
tiempo['largo'] = fuzz.trimf(tiempo.universe, [15, 30, 30])

salida['baja'] = fuzz.trimf(salida.universe, [0, 0, 40])
salida['moderada'] = fuzz.trimf(salida.universe, [30, 50, 70])
salida['alta'] = fuzz.trimf(salida.universe, [60, 100, 100])

rule1 = ctrl.Rule(temp_agua['fria'] & tiempo['corto'], salida['baja'])
rule2 = ctrl.Rule(temp_agua['templada'] & tiempo['medio'], salida['moderada'])
rule3 = ctrl.Rule(temp_agua['caliente'] & tiempo['largo'], salida['alta'])

sistema = ctrl.ControlSystem([rule1, rule2, rule3])
simulacion = ctrl.ControlSystemSimulation(sistema)

# Parte del problema

simulacion.input['temp_agua'] = 25
simulacion.input['tiempo'] = 15

simulacion.compute()
resultado = simulacion.output['salida']

# Grado de pertenencia del valor defuzzificado
mu_baja = fuzz.interp_membership(
    salida.universe, salida['baja'].mf, resultado)

mu_moderada = fuzz.interp_membership(
    salida.universe, salida['moderada'].mf, resultado)

mu_alta = fuzz.interp_membership(
    salida.universe, salida['alta'].mf, resultado)

print(f"Resultado numérico: {resultado:.2f}")
print(f"Pertenencia a BAJA: {mu_baja:.2f}")
print(f"Pertenencia a MODERADA: {mu_moderada:.2f}")
print(f"Pertenencia a ALTA: {mu_alta:.2f}")