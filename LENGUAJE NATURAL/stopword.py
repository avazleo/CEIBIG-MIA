import nltk
import ssl

# Mantenga el parche de SSL que usamos antes si sigue en la misma red
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Descarga de los tres recursos necesarios
nltk.download('punkt')
nltk.download('punkt_tab')  # <--- Esta es la línea crucial ahora
nltk.download('stopwords')

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# 1. Definimos un texto de entrada (un titular de tecnología)
titular = "La Inteligencia Artificial es una de las áreas más fascinantes de la tecnología actual."

# 2. Tokenización: Convertimos el texto a una lista de palabras en minúsculas
tokens = word_tokenize(titular.lower(), language='spanish')

# 3. Cargamos las stopwords del español
palabras_vacias = set(stopwords.words('spanish'))

# 4. Filtramos: mantenemos solo las palabras que NO están en la lista de stopwords
texto_filtrado = [palabra for palabra in tokens if palabra not in palabras_vacias and palabra.isalnum()]

#for palabra in tokens:
#    if palabra not in palabras_vacias and palabra.isalnum():
#        texto_filtrado.append(palabra)

print(f"Tokens originales ({len(tokens)}):")
print(tokens)

print(f"\nTokens tras eliminar stopwords ({len(texto_filtrado)}):")
print(texto_filtrado)