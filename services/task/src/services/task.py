import logging
from ..exceptions import ResourceNotFound
from src.models.task import Task
import requests 
logger = logging.getLogger(__name__)
from src import db
from sqlalchemy.sql import select
from datetime import datetime

from decimal import Decimal
        
class TaskService:
    """Task Service"""

    def get_by_id(self, id: int):
        task = Task.query.filter_by(id=id).first()
        if not task:
            logger.info("Task: Task Not found with id {id}".format(id=id))
            raise ResourceNotFound(
                message="Task Not found with id: {id}".format(id=id)
            )
        return task

    def get_all(self):
        tasks = [p.to_json() for p in Task.query.order_by(Task.id.asc())]
        return tasks


    def update(self, id, payload):
        task = self.get_by_id(id)
        task = task.update(payload, commit=True)
        logger.info(
            "Task: Task with id: {id} update successfuly".format(id=id)
        )
        return task
    
    def create(self, payload):
      
        task = Task(
            description=payload.get("description"),
        )
        task.save()
        logger.info(
            "Task: task created successfuly".format(id=id)
        )
        return task



task_service = TaskService()
