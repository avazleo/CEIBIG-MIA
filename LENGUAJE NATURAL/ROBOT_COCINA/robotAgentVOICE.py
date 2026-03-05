import speech_recognition as sr
import spacy
import re

# Cargamos el motor de procesamiento de lenguaje natural
nlp = spacy.load("es_core_news_sm")


class RobotCocinaVoz:
    def __init__(self):
        self.mapeo_acciones = {
            "cocer": "CALOR", "hervir": "CALOR", "calentar": "CALOR",
            "batir": "AGITAR", "remover": "AGITAR", "agitar": "AGITAR",
            "parar": "STOP", "detener": "STOP"
        }
        self.r = sr.Recognizer()

    def capturar_voz(self):
        """Escucha el micrófono y convierte el audio en texto"""
        with sr.Microphone() as source:
            print("\n[Robot] Escuchando... (Diga su comando)")
            # Ajuste de ruido ambiental
            self.r.adjust_for_ambient_noise(source, duration=0.5)
            audio = self.r.listen(source)

        try:
            # Enviamos el audio al motor de ASR (Google Web Speech API)
            texto = self.r.recognize_google(audio, language="es-ES")
            print(f"[ASR] Usted ha dicho: '{texto}'")
            return texto
        except sr.UnknownValueError:
            print("[Error] No he podido entender el audio.")
            return None
        except sr.RequestError:
            print("[Error] Problemas de conexión con el servicio ASR.")
            return None

    def extraer_instrucciones(self, texto):
        """Mismo motor de PLN desarrollado anteriormente"""
        doc = nlp(texto.lower())
        instrucciones = {"accion": "DESCONOCIDA", "temp": 0, "vel": 0, "tiempo": 0}

        # Lógica de extracción de acción y parámetros
        for token in doc:
            if token.lemma_ in self.mapeo_acciones:
                instrucciones["accion"] = self.mapeo_acciones[token.lemma_]

        # Regex para parámetros específicos
        temp = re.search(r'(\d+)\s*(grados|º)', texto)
        vel = re.search(r'(velocidad|vel)\s*(\d+)', texto)
        tiempo = re.search(r'(\d+)\s*(minutos|min)', texto)

        if temp: instrucciones["temp"] = int(temp.group(1))
        if vel: instrucciones["vel"] = int(vel.group(2))
        if tiempo: instrucciones["tiempo"] = int(tiempo.group(1))

        return instrucciones


# --- Bucle Principal de la 'Clase' ---
robot = RobotCocinaVoz()

while True:
    comando_voz = robot.capturar_voz()
    if comando_voz:
        if "adiós" in comando_voz or "salir" in comando_voz:
            print("Apagando sistema...")
            break

        resultado = robot.extraer_instrucciones(comando_voz)
        print(f"==> EJECUTANDO: {resultado}")