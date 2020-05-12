import logging
from flask import Flask,Blueprint, jsonify, request
from flask_restful import Resource, Api, reqparse

from ..services.task import task_service
tasks_blueprint = Blueprint('tasks', __name__)
api = Api(tasks_blueprint)
logger = logging.getLogger(__name__)


@tasks_blueprint.route('/tasks/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


class TaskResources(Resource):
    """Task resources"""
    def __init__(self):
         
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('description', type=str, location='json')
      
        super(TaskResources, self).__init__()

    def get(self):
        """Get all tasks """
        response = dict()
        tasks = task_service.get_all()
        response['results'] = tasks
        response['count'] = len(tasks)
   
        return response, 200

    def post(self):
        """Create new people"""
        response = dict()
        
        # parser = reqparse.RequestParser(bundle_errors=True)
        # parser.add_argument('description', type=str)
        # data = parser.parse_args()
        # data = self.parser.parse_args()
        
        json_data = request.get_json(force=True)
        un = json_data['description']
        response['un'] = un
        task = task_service.create(json_data)
        response['status'] = 'success'
        response['message'] = 'task was created successfully'
    
        return response, 202
        


class TaskDetailResources(Resource):
    """Task Detail resources"""

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            'description', type=str, location='json', required=True
        )
        super(TaskDetailResources, self).__init__()

    def get(self, task_id):
        """Get detail task"""
        response = dict()
        task = task_service.get_by_id(id=task_id)
        response = task.to_json()
        return response, 200

    def put(self, task_id):
        response = dict()
        json_data = request.get_json(force=True)
        
        print(json_data)
        # data = self.parser.parse_args()
        
    
        if 'description' not in json_data:
            err_msg = "Task: Bad request in update task {}, description field is mandatory".format(
                task_id
            )
            response['message'] = err_msg
            response['error'] = True
            return response, 400
        else:
            data = json_data['description']
            response['json input'] = data
            task = task_service.update(task_id, json_data)
            response['status'] = 'success'
            response['message'] = 'Task was updated!'
            response["data"] = task.to_json()
            return response, 200
        
        
api.add_resource(TaskResources, '/v1/tasks/')
api.add_resource(TaskDetailResources, '/v1/tasks/<task_id>')

