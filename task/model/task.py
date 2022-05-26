from datetime import datetime, timedelta
from peewee import *

# config
DATABASE = 'task.db'
DEBUG = True
SECRET_KEY = 'zow6bab8ge20*r=x&arsmp+5$0kn=-#log$pt^#@vrqjld!^2cp@g*a'

database = SqliteDatabase(DATABASE)

class BaseModel(Model):
    class Meta:
        database = database


class Task(BaseModel):
    title = CharField(unique=True)
    due_date = DateTimeField(index=True)

    class Meta:
        order_by = ('-due_date',)

    def get(task_id):
        row = Task.select().where(Task.id == task_id)
        return row[0] if row.count() > 0 else None


    def expire_in_days(delta):
        return (Task
                .select()
                .where(Task.due_date <= (datetime.now() + timedelta(days=delta)))
                )

with database:
    database.create_tables([Task], safe=True)


