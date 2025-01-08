from sqlmodel import Session

def create_entity(session: Session, entity):
    session.add(entity)
    session.commit()
    session.refresh(entity)
    return entity

def read_entities(session: Session, model, filter_by=None):
    query = session.query(model)
    if filter_by:
        query = query.filter(filter_by)
    return query.all()

def update_entity(session: Session, entity, updates: dict):
    for key, value in updates.items():
        setattr(entity, key, value)
    session.add(entity)
    session.commit()
    session.refresh(entity)
    return entity

def delete_entity(session: Session, entity):
    session.delete(entity)
    session.commit()
    return True
