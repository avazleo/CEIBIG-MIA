from langdetect import detect_langs, detect
from langdetect import DetectorFactory
from textblob import TextBlob


DetectorFactory.seed = 0  # Esto garantiza resultados consistentes

print("Porcentaje de idioma: ", detect_langs("Spain is different"))
print("Porcentaje de idioma: ", detect_langs("España es diferente"))
print("Idioma: ", detect("Spain is different"))
print("Idioma: ", detect("España es diferente"))

str = "whaat ixs yoor nami"
new_doc = TextBlob(str)
result = new_doc.correct()
print(result)
