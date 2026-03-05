# Estado interno del agente (modelo del mundo)
state = {
    "location": "A",
    "A": "dirty",
    "B": "dirty"
}

# Última acción realizada
action = None

# Modelos del entorno
def transition_model(state, action):
    """Simula cómo cambia el estado tras una acción."""
    new_state = state.copy()
    if action == "move to A":
        new_state["location"] = "A"
    elif action == "move to B":
        new_state["location"] = "B"
    elif action == "clean":
        new_state[state["location"]] = "clean"
    return new_state

def sensor_model(percept):
    """Actualiza lo que percibe el agente del entorno."""
    location, status = percept
    return {location: status, "location": location}

# Actualiza el estado interno
def update_state(state, action, percept, transition_model, sensor_model):
    sensed = sensor_model(percept)
    updated = state.copy()
    updated.update(sensed)
    if action:
        updated = transition_model(updated, action)
    return updated

# Reglas del agente
class Rule:
    def __init__(self, condition, action):
        self.condition = condition
        self.action = action

def rule_match(state, rules):
    for rule in rules:
        if rule.condition(state):
            return rule
    return None

rules = [
    Rule(lambda s: s[s["location"]] == "dirty", "clean"),
    Rule(lambda s: s[s["location"]] == "clean" and s["location"] == "A", "move to B"),
    Rule(lambda s: s[s["location"]] == "clean" and s["location"] == "B", "move to A")
]

# Programa del agente
def model_based_reflex_agent_program(percept):
    global state, action
    state = update_state(state, action, percept, transition_model, sensor_model)
    rule = rule_match(state, rules)
    action = rule.action if rule else "do nothing"
    return action

# Simulación de percepciones del entorno
percepciones = [("A", "dirty"), ("A", "clean"), ("B", "dirty"), ("B", "clean")]

for p in percepciones:
    act = model_based_reflex_agent_program(p)
    print(f"Percepción: {p} → Acción: {act} → Estado: {state}")