import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz

temp_universe = np.arange(0, 61, 1)
time_universe = np.arange(0, 31, 1)
out_universe  = np.arange(0, 101, 1)

temp_fria     = fuzz.trimf(temp_universe, [0, 0, 20])
temp_templada = fuzz.trimf(temp_universe, [15, 27, 40])
temp_caliente = fuzz.trimf(temp_universe, [30, 60, 60])

time_corto = fuzz.trimf(time_universe, [0, 0, 10])
time_medio = fuzz.trimf(time_universe, [5, 12, 20])
time_largo = fuzz.trimf(time_universe, [15, 30, 30])

out_baja     = fuzz.trimf(out_universe, [0, 0, 40])
out_moderada = fuzz.trimf(out_universe, [30, 50, 70])
out_alta     = fuzz.trimf(out_universe, [60, 100, 100])

plt.figure()
plt.plot(temp_universe, temp_fria, label="Fría")
plt.plot(temp_universe, temp_templada, label="Templada")
plt.plot(temp_universe, temp_caliente, label="Caliente")
plt.title("Funciones de pertenencia - Temperatura del agua (°C)")
plt.xlabel("Temperatura (°C)"); plt.ylabel("μ"); plt.grid(True); plt.legend()
plt.show()

plt.figure()
plt.plot(time_universe, time_corto, label="Corto")
plt.plot(time_universe, time_medio, label="Medio")
plt.plot(time_universe, time_largo, label="Largo")
plt.title("Funciones de pertenencia - Tiempo de ducha (min)")
plt.xlabel("Tiempo (min)"); plt.ylabel("μ"); plt.grid(True); plt.legend()
plt.show()

plt.figure()
plt.plot(out_universe, out_baja, label="Baja")
plt.plot(out_universe, out_moderada, label="Moderada")
plt.plot(out_universe, out_alta, label="Alta")
plt.title("Funciones de pertenencia - Salida (0–100)")
plt.xlabel("Salida"); plt.ylabel("μ"); plt.grid(True); plt.legend()
plt.show()