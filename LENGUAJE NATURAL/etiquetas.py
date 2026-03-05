from nltk.tokenize import word_tokenize
import nltk

text = word_tokenize("And from now on this will be completely different")
#print(nltk.pos_tag(text))
etiquetas = nltk.pos_tag(text)

numeros = []
for t in etiquetas:
    if 'RB' in t:
        numeros.append(t[0])
print(etiquetas)
print(numeros)