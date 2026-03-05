def table_driven_agent_program(table, current_percept, past_percepts=[]):
    past_percepts.append(current_percept)
    percept = tuple(past_percepts)
    action = table.get(percept)
    if action is None:
        action = table.get(tuple())
    return action

def main():
    # Tabla de acciones del agente
    table = {
        tuple(): "esperar",  # acción por defecto si no hay percepción previa
        ("luz encendida",): "apagar luz",
        ("luz apagada",): "encender luz",
        ("luz encendida", "luz apagada"): "intermitente",
        ("luz encendida", "luz apagada", "luz encendida"): "bombilla rota",
    }

    # Simulación de percepciones
    percepciones = ["luz encendida", "luz apagada", "luz encendida"]

    past_percepts = []  # historial de percepciones

    for p in percepciones:
        accion = table_driven_agent_program(table, p, past_percepts)
        print(f"Percepción: {p} → Acción: {accion}")


if __name__ == "__main__":
    main()