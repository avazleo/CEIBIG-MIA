def table_driven_agent_program(table, current_percept):
    action = table.get((current_percept,))
    if action is None:
        action = table.get(tuple())
    return action


def main():
    # Tabla de acciones del agente
    table = {
        tuple(): "esperar",  # acción por defecto si no hay percepción previa
        ("luz encendida",): "apagar luz",
        ("luz apagada",): "encender luz",
        ("luz encendida", "luz apagada"): "esperar",
    }

    # Simulación de percepciones
    percepciones = ["luz encendida", "luz apagada", "luz encendida"]


    for p in percepciones:
        accion = table_driven_agent_program(table, p)
        print(f"Percepción: {p} → Acción: {accion}")

if __name__ == "__main__":
    main()