import datetime

from flask import Flask
from flask_restful import reqparse, abort, Api, Resource, fields, marshal_with

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

res_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'due_date': fields.String
}

def abort_if_task_doesnt_exist(id):
    item = Task.get(id)
    if item is None:
        abort(404, message="task {} doesn't exist".format(id))

# task
# shows a single task item and lets you delete a task item
class TaskAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('id', type=int, location='json')
        self.reqparse.add_argument('title', type=str, location='json')
        self.reqparse.add_argument('due_date', type=str, location='json')
        super(TaskAPI, self).__init__()

    def get(self, id):
        item = Task.get(id)
        if item is None:
            abort(404, message="task {} doesn't exist".format(id))
        return item.serialize

    def delete(self, id):
        abort_if_task_doesnt_exist(id)
        del tasks[id]
        return '', 204

    def put(self, id):
        args = self.reqparse.parse_args()
        try:
            due_date = datetime.datetime.strptime(args.due_date, due_date_fmt)
        except ValueError:
            abort(400, message="due_date format error: {}".format(args.due_date))

        abort_if_task_doesnt_exist(args.id)
        Task.update(args.id, args.title, due_date)

    def post(self):
        args = self.reqparse.parse_args()
        if Task.exists(args.title):
            abort(400, message="Task {} already exists".format(args.title))

        cnt = Task.insert(title=args.title, due_date=args.due_date).execute()
        return cnt, 201

#def parse_task(args):



# taskList
# shows a list of all tasks, and lets you POST to add new tasks
class TaskListAPI(Resource):
    def get(self):
        return tasks


api.add_resource(TaskListAPI, '/tasks')
api.add_resource(TaskAPI, 
    '/task',
    '/task/<int:id>'
)

if __name__ == '__main__':
    app.run(debug=True)
