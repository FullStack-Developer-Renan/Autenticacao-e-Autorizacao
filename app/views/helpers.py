from flask import current_app


def add_commit(model) -> None:
    session = current_app.db.session
    session.add(model)
    session.commit()

def delete_commit(model) -> None:
    session = current_app.db.session
    session.delete(model)
    session.commit()