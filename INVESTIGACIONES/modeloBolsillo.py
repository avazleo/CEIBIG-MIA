from gliner2 import GLiNER2

extractor = GLiNER2.from_pretrained("fastino/gliner2-base-v1")
text = "Apple CEO Tim Cook announced iPhone 15 in Cupertino yesterday."
labels = ["company", "person", "product", "location"]
print(extractor.extract_entities(text, labels))

entity_descriptions = {
    "company": "Business organizations and corporations",
    "person": "Names of individuals",
    "location": "Geographical places (cities, countries, etc.)",
    "product": "Products, devices, services, or offerings",
}
print(extractor.extract_entities(text, entity_descriptions))

text = "The new MacBook Pro costs $1999 and comes with an M3 chip and 18GB RAM."

product_schema = (
    extractor.create_schema()
    .structure("product")
    .field("name", "str")  # Eliminamos la descripción posicional
    .field("price", "str")
    .field("features", "list")
    # Pasamos 'choices' como tercer argumento o por palabra clave
    .field("category", "str", choices=["electronics", "software", "hardware"])
    .build()
)

print(extractor.extract(text, product_schema))


from gliner import GLiNER

# Este modelo sí es multilingüe y compatible con la librería gliner estándar
model = GLiNER.from_pretrained("urchade/gliner_medium-v2.1")

text = "El nuevo MacBook Pro cuesta 1999 euros y viene con un chip M3 y 18GB de RAM."
labels = ["product", "price", "features"]

# En la versión estándar, el manejo de esquemas complejos es distinto,
# pero la extracción por etiquetas es sumamente potente en español:
entities = model.predict_entities(text, labels, threshold=0.4)

for entity in entities:
    print(f"{entity['label']}: {entity['text']}")