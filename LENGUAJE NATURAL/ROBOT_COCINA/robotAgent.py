import spacy
from spacy.matcher import PhraseMatcher
import re

# Cargamos el modelo en español
try:
    nlp = spacy.load("es_core_news_sm")
except:
    # Instrucción para el alumno: instalar con !python -m spacy download es_core_news_sm
    raise ImportError("Debe instalar el modelo de lenguaje de spaCy para español.")


class RobotCocinaPLN:
    def __init__(self):
        # Definición de sinónimos para normalización de acciones
        self.mapeo_acciones = {
            "cocer": "CALOR", "hervir": "CALOR", "calentar": "CALOR",
            "batir": "AGITAR", "remover": "AGITAR", "agitar": "AGITAR", "mezclar": "AGITAR",
            "parar": "STOP", "detener": "STOP", "apagar": "STOP"
        }
        self.limites = {"temp_max": 120, "vel_max": 10, "tiempo_max": 120}

    def procesar_comando(self, texto_usuario):
        # 1. Normalización básica (Fase 2.b)
        doc = nlp(texto_usuario.lower())

        # Estructura de control para el robot
        instrucciones = {"accion": None, "temp": 0, "vel": 0, "tiempo": 0}

        # 2. Extracción de valores numéricos (Fase 2.e)
        # Buscamos números seguidos de unidades o contextos
        numeros = [token.text for token in doc if token.like_num]

        # 3. Identificación de la acción y parámetros (Fase 2.d y 2.f)
        for token in doc:
            # Localizar el verbo de acción mediante lematización o mapeo
            if token.lemma_ in self.mapeo_acciones:
                instrucciones["accion"] = self.mapeo_acciones[token.lemma_]
            elif token.text in self.mapeo_acciones:
                instrucciones["accion"] = self.mapeo_acciones[token.text]

        # Lógica de extracción por contexto (Agregación sintagmática simple)
        texto_completo = doc.text

        # Búsqueda de temperatura
        temp_match = re.search(r'(\d+)\s*(grados|º|celsius)', texto_completo)
        if temp_match:
            instrucciones["temp"] = min(int(temp_match.group(1)), self.limites["temp_max"])

        # Búsqueda de velocidad
        vel_match = re.search(r'(velocidad|vel)\s*(\d+)', texto_completo)
        if vel_match:
            instrucciones["vel"] = min(int(vel_match.group(2)), self.limites["vel_max"])

        # Búsqueda de tiempo
        tiempo_match = re.search(r'(\d+)\s*(minutos|min|\')', texto_completo)
        if tiempo_match:
            instrucciones["tiempo"] = min(int(tiempo_match.group(1)), self.limites["tiempo_max"])

        return instrucciones


# --- Simulación de la Clase ---
robot = RobotCocinaPLN()

comandos_prueba = [
    "Pon el robot a batir a velocidad 5 durante 10 minutos",
    "Quiero cocer a 90 grados por 20 minutos",
    "¡Para el robot ahora!",
    "Remueve suavemente a velocidad 2"
]

print(f"{'COMANDO DE VOZ (ASR)':<50} | {'INSTRUCCIÓN GENERADA'}")
print("-" * 85)
for comando in comandos_prueba:
    resultado = robot.procesar_comando(comando)
    print(f"{comando:<50} | {resultado}")