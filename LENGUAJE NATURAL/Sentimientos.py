import nemo.collections.nlp as nemo_nlp

# 1. Cargamos un modelo pre-entrenado de análisis de sentimientos
# En este caso, uno basado en la arquitectura BERT
model = nemo_nlp.models.TextClassificationModel.from_pretrained(model_name="sentiment_analysis_bert")

# 2. Definimos una lista de frases para analizar
secuencias = [
    "El curso de especialización es excelente y muy completo.",
    "No estoy satisfecho con el rendimiento del algoritmo, es muy lento.",
    "La clase de hoy trata sobre modelos de lenguaje."
]

# 3. Realizamos la inferencia
predicciones = model.classifytext(queries=secuencias, batch_size=3)

# 4. Mostramos los resultados
for frase, etiqueta in zip(secuencias, predicciones):
    print(f"Frase: '{frase}' -> Sentimiento: {etiqueta}")