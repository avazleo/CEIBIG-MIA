import time
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

# 1. Configuración de la conexión
client = RemoteAPIClient()
sim = client.getObject('sim')
sim.startSimulation()

# 2. Obtenemos el acceso al cubo
h = sim.getObject('/Cuboid')

print("Controlador activo. Mueve el cubo en el eje Y (verde) para ver el cambio.")

try:
    while True:
        posicion = sim.getObjectPosition(h, -1)
        y_actual = posicion[1]

        # Añadimos esta línea para ver los valores en la Terminal
        print(f"Posición Y: {y_actual:.2f}", end='\r')

        # Bajamos el umbral a 0.5 para que sea más fácil de activar
        if abs(y_actual) > 0.5:
            sim.setShapeColor(h, None, sim.colorcomponent_ambient_diffuse, [1, 1, 0])
        else:
            sim.setShapeColor(h, None, sim.colorcomponent_ambient_diffuse, [0, 1, 0])

        time.sleep(0.05)

except KeyboardInterrupt:
    # Al pulsar Ctrl+C detenemos todo limpiamente
    sim.stopSimulation()
    print("\nSimulación finalizada por el usuario.")