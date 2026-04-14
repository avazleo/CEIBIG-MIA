import time
import math
import re
import speech_recognition as sr
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

# === 1. MAPEO SEMÁNTICO ===
MAPEO_ACCIONES = {
    "avanza": "AVANZAR", "camina": "AVANZAR", "tira": "AVANZAR", "muévete": "AVANZAR",
    "gira": "GIRAR", "dobla": "GIRAR", "rota": "GIRAR",
    "para": "STOP", "detente": "STOP", "quieto": "STOP", "stop": "STOP"
}

# === 2. CONFIGURACIÓN COPPELIA ===
client = RemoteAPIClient()
sim = client.getObject('sim')
robot = sim.getObject('/PioneerP3DX')
motor_izq = sim.getObject('/PioneerP3DX/leftMotor')
motor_der = sim.getObject('/PioneerP3DX/rightMotor')

v_lineal_actual = 0.0


def actuar(izq, der):
    sim.setJointTargetVelocity(motor_izq, izq)
    sim.setJointTargetVelocity(motor_der, der)


def extraer_numero(texto):
    """Busca cualquier número (entero o decimal) en el texto"""
    numeros = re.findall(r"[-+]?\d*\.\d+|\d+", texto)
    return float(numeros[0]) if numeros else None


def procesar_comando(texto_voz):
    global v_lineal_actual
    texto_voz = texto_voz.lower()

    # 1. IDENTIFICAR ACCIÓN
    accion_detectada = None
    for comando_clave, valor in MAPEO_ACCIONES.items():
        if comando_clave in texto_voz:
            accion_detectada = valor
            break

    if not accion_detectada:
        return "❓ Comando no reconocido."

    # 2. LÓGICA DE STOP
    if accion_detectada == "STOP":
        v_lineal_actual = 0.0
        actuar(0, 0)
        return "🛑 STOP: Robot detenido."

    # 3. LÓGICA DE AVANCE (CON VELOCIDAD)
    elif accion_detectada == "AVANZAR":
        velocidad = extraer_numero(texto_voz)
        if velocidad is None: velocidad = 0.5  # Velocidad por defecto si no dice número

        v_lineal_actual = velocidad
        actuar(v_lineal_actual, v_lineal_actual)
        return f"🚀 AVANZANDO a {v_lineal_actual} m/s."

    # 4. LÓGICA DE GIRO (DIRECCIÓN Y GRADOS)
    elif accion_detectada == "GIRAR":
        grados = extraer_numero(texto_voz)
        if grados is None: grados = 90

        # DETERMINAR DIRECCIÓN (Derecha es negativo en Pioneer para rotar)
        sentido = 0
        if "derecha" in texto_voz:
            sentido = -1
            dir_str = "DERECHA"
        elif "izquierda" in texto_voz:
            sentido = 1
            dir_str = "IZQUIERDA"
        else:
            return "🤔 ¿Hacia qué lado? (Dime izquierda o derecha)"

        v_rot = 1.0  # Velocidad de rotación constante
        # Tiempo = Distancia angular / Velocidad angular
        tiempo_giro = (abs(grados) * (math.pi / 180)) / v_rot

        # GIRAR: Si está parado, pivota. Si avanza, hace curva.
        actuar(v_lineal_actual - (sentido * v_rot), v_lineal_actual + (sentido * v_rot))
        time.sleep(tiempo_giro)
        actuar(v_lineal_actual, v_lineal_actual)  # Vuelve a su velocidad previa

        return f"🔄 GIRO: {grados}° a la {dir_str}."


# === 3. ESCUCHA ACTIVA ===
recognizer = sr.Recognizer()
recognizer.pause_threshold = 0.5
mic = sr.Microphone()

sim.startSimulation()

# Aseguramos que el robot esté quieto antes de empezar a escuchar
actuar(0, 0)
v_lineal_actual = 0.0
print("🤖 Motores inicializados a 0. Calibrando...")

with mic as source:
    recognizer.adjust_for_ambient_noise(source, duration=1)
    print("🎙️ LISTO. Ejemplo: 'Avanza a 1.5', 'Gira a la derecha 90 grados'...")

    while True:
        try:
            audio = recognizer.listen(source, phrase_time_limit=4, )
            texto = recognizer.recognize_google(audio, language="es-ES")
            print(f"Escuchado: {texto}")

            resultado = procesar_comando(texto)
            print(resultado)
            sim.addStatusbarMessage(resultado)

        except sr.UnknownValueError:
            pass
        except KeyboardInterrupt:
            break

sim.stopSimulation()