"""Curadoria semiautomática: validação e ajuste dos dados extraídos."""

def validate_entities(entities):
    valid = []
    for ent in entities:
        if len(ent[0]) > 2:  # Filtro simples
            valid.append(ent)
    return valid
