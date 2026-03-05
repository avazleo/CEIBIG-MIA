import spacy

# Cargamos el modelo exactamente con el nombre del fichero instalado
nlp = spacy.load('es_core_news_sm')

doc = nlp('Ella comio pizza')

for token in doc:
    print(f"Token: {token.text:10} | Categoría: {token.pos_}")