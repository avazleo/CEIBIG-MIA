import nltk

texto = "We are living special moments"
tokens = nltk.word_tokenize(texto)

# Este es posiblemente el algoritmo más famoso
porter = nltk.PorterStemmer()
print ([porter.stem(t) for t in tokens])

# Este es otro de los algoritmos más famosos
lancaster = nltk.LancasterStemmer()
print ([lancaster.stem(t) for t in tokens])