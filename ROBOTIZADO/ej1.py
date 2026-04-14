import time
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

client = RemoteAPIClient()
sim = client.getObject('sim')

sim.startSimulation()

# Esperamos un momento a que el simulador responda al "Play"
time.sleep(1)

h = sim.getObject('/Cuboid')

# Intentamos el amarillo [1, 1, 0]
print("Enviando orden de color amarillo...")
sim.setShapeColor(h, None, sim.colorcomponent_ambient_diffuse, [1, 1, 0])

# Mantenemos vivo el script para ver el resultado
time.sleep(2)