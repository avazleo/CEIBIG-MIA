from nltk.corpus import wordnet

synsets=wordnet.synsets('big')
print(synsets[0].definition())
print(synsets[0].examples())

# Buscamos los synsets de la palabra 'grande' en español
synsets = wordnet.synsets('grande', lang='spa')

if synsets:
    # Tomamos el primer concepto (synset) encontrado
    primer_synset = synsets[0]

    print(f"Concepto: {primer_synset.name()}")
    print(f"Definición: {primer_synset.definition()}")
    print(f"Ejemplos: {primer_synset.examples()}")

    # Opcional: Ver otros términos en español vinculados a este concepto
    lemas_spa = [l.name() for l in primer_synset.lemmas(lang='spa')]
    print(f"Sinónimos en español para este concepto: {lemas_spa}")
else:
    print("No se encontraron conceptos para esa palabra.")