import matplotlib.pyplot as plt
from sklearn import tree
import pandas as pd

# 1. Preparación de datos (Dataset de entrenamiento)
# Características (Features): [Edad, Tiene_Nomina, Indefinido, Duracion_Contrato_Suficiente]
# Nota: Hemos codificado las variables categóricas en valores numéricos (0 y 1)
X = [
    [25, 1, 1, 1], # Concedido
    [17, 1, 1, 1], # Denegado (menor de 18)
    [30, 0, 1, 1], # Denegado (sin nómina)
    [40, 1, 0, 0], # Denegado (temporal corto)
    [35, 1, 0, 1], # Concedido (temporal largo)
    [19, 1, 1, 1]  # Concedido
]

# Etiquetas (Labels): 1 = Concedido, 0 = Denegado
y = [1, 0, 0, 0, 1, 1]

# 2. Entrenamiento del Clasificador
clf = tree.DecisionTreeClassifier(criterion='entropy', random_state=42)
clf = clf.fit(X, y)

# 3. Visualización del Árbol (Inspección previa)
print("Generando estructura lógica del modelo...")
nombres_caracteristicas = ['Edad', 'Tiene Nomina', 'Indefinido', 'Contrato > Plazo']
nombres_clases = ['DENEGADO', 'CONCEDIDO']

# Aumentamos los DPI (puntos por pulgada) para que no se vea pixelado
plt.figure(figsize=(15, 10), dpi=300)

tree.plot_tree(clf,
               feature_names=nombres_caracteristicas,
               class_names=nombres_clases,
               filled=True,
               rounded=True,
               fontsize=10, # Ajustamos el tamaño de fuente para que no se solape
               precision=2) # Limitamos los decimales para limpiar visualmente los nodos

plt.title("Estructura Lógica del Clasificador (Alta Resolución)")
plt.savefig("arbol_decision.png", bbox_inches='tight') # Lo guarda como archivo nítido
plt.show()

# 4. Toma de decisión con un nuevo cliente
print("\n--- Evaluación de Nuevo Cliente ---")
# Datos del cliente: 25 años, tiene nómina (1), contrato temporal (0), duración suficiente (1)
nuevo_cliente = [[25, 1, 0, 1]]
prediccion = clf.predict(nuevo_cliente)
probabilidad = clf.predict_proba(nuevo_cliente)

# 5. Conclusión final
resultado = nombres_clases[prediccion[0]]
print(f"Datos del cliente: {nuevo_cliente}")
print(f"Conclusión del modelo: {resultado}")
print(f"Confianza de la predicción: {probabilidad[0][prediccion[0]] * 100}%")