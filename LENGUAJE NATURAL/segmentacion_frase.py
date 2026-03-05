from nltk.tokenize import sent_tokenize

EJEMPLO_FRASES = "Hola mi nombre es Pepe. Mi casa no estoy seguro de dónde está."
frases = sent_tokenize(EJEMPLO_FRASES)
for frase in frases:
    print(frase)
