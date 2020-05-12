from src import db
from src.models.task import Task


def add_task(description):
    task = Task(
        description=description
    )
    db.session.add(task)
    db.session.commit()
    return task

