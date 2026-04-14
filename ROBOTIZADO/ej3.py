import time
import math
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

# === 1. CONEXIÓN Y CONFIGURACIÓN ===
client = RemoteAPIClient()
sim = client.getObject('sim')

# Obtenemos el handle del cubo
h = sim.getObject('/Cuboid')

# ESTADO INICIAL: Posición origen y color verde
sim.setObjectPosition(h, -1, [0, 0, 0.05])
sim.setShapeColor(h, None, sim.colorcomponent_ambient_diffuse, [0, 1, 0])

# Variables para la lógica
penalizaciones = 0
tiempo_inicio = time.time()

# Arrancamos la simulación
sim.startSimulation()
print("SISTEMA INICIADO: El cubo se mueve solo. Revisa la consola de CoppeliaSim.")

# === 2. BUCLE PRINCIPAL ===
try:
    while True:
        # A. MOVIMIENTO: Calculamos la nueva posición Y (oscilación)
        t = time.time() - tiempo_inicio
        y_auto = math.sin(t * 1.5) * 2  # Se mueve entre -2 y 2 metros

        # Aplicamos el movimiento manteniendo X=0 y Z=0.05
        sim.setObjectPosition(h, -1, [0, y_auto, 0.05])

        # B. LÓGICA DE CONTROL Y LOGS EN TIEMPO REAL
        distancia = abs(y_auto)

        if distancia > 1.5:
            # ZONA ROJA: Error crítico
            sim.setShapeColor(h, None, sim.colorcomponent_ambient_diffuse, [1, 0, 0])
            penalizaciones += 1
            sim.addLog(sim.verbosity_errors, f"!!! INFRACCIÓN CRÍTICA !!! Total: {penalizaciones}")

        elif distancia > 0.8:
            # ZONA AMARILLA: Advertencia
            sim.setShapeColor(h, None, sim.colorcomponent_ambient_diffuse, [1, 1, 0])
            sim.addLog(sim.verbosity_warnings, "Precaución: Saliendo de la zona segura")

        else:
            # ZONA VERDE: Todo OK
            sim.setShapeColor(h, None, sim.colorcomponent_ambient_diffuse, [0, 1, 0])

        # Monitor local en la terminal de Python
        print(f"Posición Y: {y_auto:.2f} | Penalizaciones: {penalizaciones}", end='\r')

        time.sleep(0.02)

except KeyboardInterrupt:
    sim.stopSimulation()
    print(f"\nSIMULACIÓN FINALIZADA. Penalizaciones totales: {penalizaciones}")