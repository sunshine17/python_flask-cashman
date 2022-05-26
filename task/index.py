import datetime

from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

tasks = {
    'task1': {'task': 'build an API'},
    'task2': {'task': '?????'},
    'task3': {'task': 'profit!'},
}

from task.model.task import *

def abort_if_task_doesnt_exist(task_id):
    if Task.select().where(Task.id == task_id).count() is 0:
        abort(404, message="task {} doesn't exist".format(task_id))

parser = reqparse.RequestParser()
parser.add_argument('task')


# task
# shows a single task item and lets you delete a task item
class task(Resource):
    def get(self, task_id):
        item = Task.get(task_id)
        if item is None:
            abort(404, message="task {} doesn't exist".format(task_id))
        return item

    def delete(self, task_id):
        abort_if_task_doesnt_exist(task_id)
        del tasks[task_id]
        return '', 204

    def put(self, task_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        tasks[task_id] = task
        return task, 201

    def post(self):
        args = parser.parse_args()
        return [args.title, args.due_date], 201

# taskList
# shows a list of all tasks, and lets you POST to add new tasks
class taskList(Resource):
    def get(self):
        return tasks


api.add_resource(taskList, '/tasks')
api.add_resource(task, '/task')

if __name__ == '__main__':
    app.run(debug=True)
