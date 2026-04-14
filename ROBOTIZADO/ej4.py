import time
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

client = RemoteAPIClient()
sim = client.getObject('sim')
h = sim.getObject('/Cuboid')


def preparar():
    sim.stopSimulation()
    time.sleep(0.5)
    sim.setObjectPosition(h, -1, [0, 1.5, 0.05])  # Empezamos fuera del centro
    sim.startSimulation()


# Estado global para la memoria del sistema experto
esta_recargando = False

# === VARIABLE DE CONTROL DE LOG ===
ultimo_estado = ""

def enviar_log(sim, estado, nivel="INFO"):
    """
    Envía un mensaje formateado a la Status Bar de CoppeliaSim.
    Niveles sugeridos: INFO, WARNING, OK
    """
    prefijos = {
        "INFO": "[ℹ️ INFO]",
        "WARNING": "[⚠️ ALERTA]",
        "OK": "[✅ EXITO]",
        "CARGA": "[⚡ CARGANDO]"
    }
    mensaje = f"{prefijos.get(nivel, 'INFO')} {estado}"
    # Cambiamos addLogStatusbar por addStatusbarMessage
    sim.addStatusbarMessage(mensaje)


def motor_experto_pro(y, bat):
    global esta_recargando
    K = 0.8
    ZONA_CARGA = -2.5

    # LOGICA DE ESTADOS CON HISTÉRESIS
    if bat < 20:
        esta_recargando = True
    if bat > 90:
        esta_recargando = False

    # REGLA 1: ESTADO DE EMERGENCIA / CARGA
    if esta_recargando:
        dist_carga = ZONA_CARGA - y
        if abs(dist_carga) < 0.1:
            return 0.0, [1, 1, 1], "CARGANDO..."
        return 0.6, [1, 0, 0], "BUSCANDO ENERGÍA"

    # REGLA 2: ESTADO NORMAL (Vigilancia del centro)
    dist_centro = abs(y)
    if dist_centro < 0.05:
        return 0.0, [0, 1, 0], "OBJETIVO LOGRADO"

    v_prop = min(dist_centro * K, 1.5)
    return v_prop, [0, 0.5, 1], "CORRIGIENDO"


preparar()
bateria = 40.0  # Nivel inicial para ver el ciclo rápido
t_prev = time.time()

try:
    while True:
        t_act = time.time()
        dt = t_act - t_prev
        y_act = sim.getObjectPosition(h, -1)[1]

        v_cmd, rgb, estado_actual = motor_experto_pro(y_act, bateria)

        # Lógica de Log por Gravedad
        if estado_actual != ultimo_estado:
            if "CARGANDO" in estado_actual:
                enviar_log(sim, f"Iniciando proceso de recarga. Batería al {round(bateria)}%", "CARGA")
            elif "ENERGÍA" in estado_actual:
                enviar_log(sim, "Nivel crítico detectado. Buscando estación...", "WARNING")
            elif "LOGRADO" in estado_actual:
                enviar_log(sim, "Posición nominal alcanzada.", "OK")
            else:
                enviar_log(sim, f"Estado: {estado_actual}", "INFO")

            ultimo_estado = estado_actual

        if estado_actual == "CARGANDO...":
            bateria = min(bateria + 15.0 * dt, 100.0)  # Carga rápida para la clase
        else:
            target = -2.5 if esta_recargando else 0.0
            dir = 1 if target > y_act else -1
            sim.setObjectPosition(h, -1, [0, y_act + (dir * v_cmd * dt), 0.05])
            # Gasto aumentado para que el ciclo sea visible
            bateria -= (1.5 + v_cmd * 2) * dt

        sim.setShapeColor(h, None, sim.colorcomponent_ambient_diffuse, rgb)
        print(f"Batería: {bateria:5.1f}% | Estado: {estado_actual:15}", end='\r')

        t_prev = t_act
        time.sleep(0.01)

except KeyboardInterrupt:
    sim.stopSimulation()