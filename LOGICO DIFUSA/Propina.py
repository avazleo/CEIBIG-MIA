import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Rangos de valores que pueden tomar las variables difusas
food_quality = ctrl.Antecedent(np.arange(0, 11, 1), 'calidad de la comida')
service_quality = ctrl.Antecedent(np.arange(0, 11, 1), 'calidad del servicio')
tip = ctrl.Consequent(np.arange(0, 26, 1), 'propina')

# Indicamos que genere 3 funciones de pertenencia automaticamente para cada
# antecedente con las etiquetas lingüisticas indicadas
food_quality.automf(names=['mala', 'decente', 'buena'])
service_quality.automf(names=['pobre', 'aceptable', 'increible'])

# Definimos manualmente las funciones de pertenencia utilizando conjuntos
# triangulares para el consecuente; los puntos del triángulo se introducen en
# sentido horario comenzando por el extremo izquierdo
tip['baja'] = fuzz.trimf(tip.universe, [0, 0, 13])
tip['media'] = fuzz.trimf(tip.universe, [0, 13, 25])
tip['alta'] = fuzz.trimf(tip.universe, [13, 25, 25])

# Definimos las reglas y las asociamos con el sistema
tipping = ctrl.ControlSystemSimulation(ctrl.ControlSystem([
ctrl.Rule(food_quality['mala'] | service_quality['pobre'], tip['baja']),
ctrl.Rule(service_quality['aceptable'], tip['media']),
ctrl.Rule(food_quality['buena'] | service_quality['increible'], tip['alta'])
]))

# Entradas para nuestro problema concreto
tipping.inputs({
'calidad de la comida': 1.5,
'calidad del servicio': 2.8
 })

# Inferencia y defuzzificación
tipping.compute()

print(tipping.output['propina'])