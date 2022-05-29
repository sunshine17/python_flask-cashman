import datetime as dt
from functools import wraps
from flask_restful import abort, Api, Resource 

from flask import Flask, request, g, jsonify
import peewee as pw
from marshmallow import (
    Schema,
    fields,
    validates,
    ValidationError,
)

import logging
 
# Create and configure logger
logging.basicConfig(filename="log.log",
	format='%(asctime)s`%(name)s`%(levelname)s`%(message)s',
	filemode='w',
	level=logging.DEBUG
)
 
logger = logging.getLogger('__main__')
logger.setLevel(logging.DEBUG)

app = Flask(__name__)
api = Api(app)
db = pw.SqliteDatabase("/tmp/task.db")

###### MODELS #####

class BaseModel(pw.Model):
    """Base model class. All descendants share the same database."""

    class Meta:
        database = db


class Task(BaseModel):
    title = pw.TextField()
    due_date = pw.DateTimeField()

    class Meta:
        order_by = ("-due_date",)


def create_tables():
    if db.is_closed:
        db.connect()
    Task.create_table(True)


##### SCHEMAS #####


DUE_DATE_FMT = "%d/%m/%Y"


class TaskSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    due_date = fields.DateTime(required=True)

    @validates("due_date")
    def validate_date(self, val):
        if type(val) is dt.datetime:
            return True
        try:
#            dt.datetime.strptime(val, DUE_DATE_FMT)
            dt.datetime.strptime(val, DUE_DATE_FMT)
            return True
        except ValueError:
            return False

def task_to_model(dic):
    if not dic:
        return None

    return Task(
        title=dic['title'],
        due_date=dic['due_date'],
    )


task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

# Ensure a separate connection for each thread
#@app.before_request
def before_request():
    g.db = db
    g.db.connect()


#@app.after_request
def after_request(response):
    g.db.close()
    return response


#### API #####


class TaskAPI(Resource):

    def get(self, id):
        try:
            task = Task.get(Task.id == id)
        except Task.DoesNotExist:
            abort(404, message="task {} doesn't exist".format(id))
        return task_schema.dump(task)

    def delete(self, id):
        q = Task.delete().where(Task.id == id)
        rows = q.execute()
        logger.info("task deleted`id={id}`affected_rows={cnt}".format(id=id, cnt=rows))
        return 200

    def put(self, id):
        try:
            task = Task.get(Task.id == id)
        except Task.DoesNotExist:
            abort(404, message="task {} doesn't exist".format(id))

        json_input = request.get_json()
        try:
            input_dic = task_schema.load(json_input, partial=("title","due_date",))

            if 'title' not in input_dic and 'due_date' not in input_dic:
                abort(400, message="nothing to update")

            if 'title' in input_dic:
                task.title = input_dic['title']
            if 'due_date' in input_dic:
                task.due_date = dt.datetime.strptime(input_dic['due_date'], DUE_DATE_FMT)
        except ValidationError as err:
            abort(400, message="input error")

        task.save()
        logger.info("task updated`id={id},obj={dic}".format(id = id, dic = input_dic))
        return '', 204

    def post(self):
        json_input = request.get_json()
        try:
            task = task_to_model(task_schema.load(json_input))
        except ValidationError as err:
            return {"errors": err.messages}, 422
        task.save()
        logger.info("new task added: {}".format(task))
        return task_schema.dump(task), 201

class TaskListAPI(Resource):
    def get(self, exp_days=None):
        if exp_days:
            return self._get_in_exp_days(exp_days)

        tasks = Task.select().order_by(Task.due_date.asc())
        return tasks_schema.dump(list(tasks))

    def _get_in_exp_days(self, exp_days):
        tasks = Task.select().where(Task.due_date <= (dt.datetime.now() + dt.timedelta(days=exp_days)))
        return tasks_schema.dump(list(tasks))

api.add_resource(TaskListAPI, 
    '/tasks', 
    '/tasks/<int:exp_days>'
)

api.add_resource(TaskAPI, 
    '/task',
    '/task/<int:id>',
)


if __name__ == "__main__":
    create_tables()
    app.run(port=5000, debug=True)
