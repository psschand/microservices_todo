import json
from werkzeug.utils import cached_property
from tests.base import BaseTestCase
from tests.utils import add_task


class TesttaskService(BaseTestCase):
    """Tests for the task Service."""

    def test_ping(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get('/tasks/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    def test_tasks(self):
        """Test tasks endpoint"""
        add_task("test1")
        add_task("test2")
        response = self.client.get('/v1/tasks/')
        data = json.loads(response.data.decode())
        print(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["count"], 2)
        self.assertEqual(data["results"][0]["description"], "test1")

    def test_tasks_not_found(self):
        """Test task endpoint"""
        unknownId = 33
        response = self.client.get('/v1/tasks/{}'.format(unknownId))
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["message"], "Task Not found with id: {}".format(unknownId))
    
    def test_tasks_by_id(self):
        """Test task endpoint"""
        add_task("Test1")
        task_id = 1
        response = self.client.get('/v1/tasks/{}'.format(task_id))
        self.assertEqual(response.status_code, 200)

    def test_update_task(self):
        """Test task endpoint"""
        add_task("Test1")
        task_id = 1
        updated_task_description = "Test1 Edit"
        response = self.client.put(
            '/v1/tasks/{}'.format(task_id),
            data=json.dumps({'description': updated_task_description}),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["data"]["description"], updated_task_description)        

