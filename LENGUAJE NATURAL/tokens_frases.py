from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk

EJEMPLO_FRASES = "Hola mi nombre es Pepe. Mi casa no estoy seguro de dónde está."
frases = sent_tokenize(EJEMPLO_FRASES)
for frase in frases:
    print(frase)
    tokens = word_tokenize(frase.lower(), language='spanish')
    [print(palabra) for palabra in tokens]

    palabras_vacias = set(stopwords.words('spanish'))
    texto_filtrado = [palabra for palabra in tokens if palabra not in palabras_vacias and palabra.isalnum()]

    porter = nltk.PorterStemmer()
    print([porter.stem(t) for t in texto_filtrado])