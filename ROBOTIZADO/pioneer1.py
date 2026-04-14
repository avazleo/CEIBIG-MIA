import time
import math
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

# === 1. CONEXIÓN ===
client = RemoteAPIClient()
sim = client.getObject('sim')

robot = sim.getObject('/PioneerP3DX')
motor_izq = sim.getObject('/PioneerP3DX/leftMotor')
motor_der = sim.getObject('/PioneerP3DX/rightMotor')
sensores = [sim.getObject(f'/PioneerP3DX/ultrasonicSensor[{i}]') for i in range(8)]


def preparar():
    sim.stopSimulation()
    time.sleep(0.5)
    sim.startSimulation()


# === 2. VARIABLES ===
en_carga = False
bateria = 25.0
ultimo_mensaje = ""


def log(msg):
    global ultimo_mensaje
    if msg != ultimo_mensaje:
        sim.addStatusbarMessage(msg)
        ultimo_mensaje = msg


preparar()

try:
    while True:
        pos = sim.getObjectPosition(robot, -1)
        orient = sim.getObjectOrientation(robot, -1)[2]
        dist_centro = math.sqrt(pos[0] ** 2 + pos[1] ** 2)

        # --- LÓGICA DE ESTADOS ---

        if bateria < 20 or en_carga:
            if not en_carga:
                log("⚠️ BATERÍA BAJA: BUSCANDO BASE")
                en_carga = True

            # FASE A: LLEGADA Y CARGA
            if dist_centro < 0.2:
                sim.setJointTargetVelocity(motor_izq, 0)
                sim.setJointTargetVelocity(motor_der, 0)
                while bateria < 100:
                    bateria += 2.0
                    log(f"⚡ CARGANDO... {round(bateria)}%")
                    time.sleep(0.15)
                en_carga = False
                log("✅ CARGA COMPLETA - REINICIANDO EXPLORACIÓN")
                continue

            # FASE B: ROTAR EN EL SITIO
            angulo_base = math.atan2(-pos[1], -pos[0])
            error = (angulo_base - orient + math.pi) % (2 * math.pi) - math.pi

            if abs(error) > 0.05:
                v_rot = 0.6 if error > 0 else -0.6
                sim.setJointTargetVelocity(motor_izq, -v_rot)
                sim.setJointTargetVelocity(motor_der, v_rot)
                log(f"🔄 BUSCANDO BASE: ROTANDO... Bat: {round(bateria)}%")

            # FASE C: AVANZAR RECTO
            else:
                sim.setJointTargetVelocity(motor_izq, 2.0)
                sim.setJointTargetVelocity(motor_der, 2.0)
                log(f"🚀 EN RUTA A BASE: AVANZANDO... Bat: {round(bateria)}%")

        else:
            # --- MODO EXPLORACIÓN ---
            hay_obstaculo = False
            for s in sensores:
                res, dist, _, _, _ = sim.readProximitySensor(s)
                if res > 0 and dist < 0.5:
                    hay_obstaculo = True;
                    break

            if hay_obstaculo:
                sim.setJointTargetVelocity(motor_izq, -1.0)
                sim.setJointTargetVelocity(motor_der, 1.0)
                log("🧱 MURO DETECTADO: ESQUIVANDO")
            else:
                sim.setJointTargetVelocity(motor_izq, 3.0)
                sim.setJointTargetVelocity(motor_der, 3.0)
                log(f"🌍 EXPLORANDO... Bat: {round(bateria)}%")

            bateria -= 0.1

        time.sleep(0.01)

except KeyboardInterrupt:
    sim.stopSimulation()