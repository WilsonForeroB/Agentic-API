def orm_to_dict(obj):
    if isinstance(obj, list):  # Si es lista, convertir cada elemento
        return [orm_to_dict(o) for o in obj]
    return {c.key: getattr(obj, c.key) for c in obj.__table__.columns}