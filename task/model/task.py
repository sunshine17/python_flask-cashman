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


due_date_fmt = "%d/%m/%Y"

class Task(BaseModel):
    title = CharField(unique=True)
    due_date = DateTimeField(index=True)

    class Meta:
        order_by = ('-due_date',)

    def exists(title):
        return Task.select().where(Task.title == title).count() > 0 

    def get(id):
        row = Task.select().where(Task.id == id)
        return row[0] if row.count() > 0 else None

    def expire_in_days(delta):
        return (Task
                .select()
                .where(Task.due_date <= (datetime.now() + timedelta(days=delta)))
                )

    # date format: 21/08/2019
    @property
    def serialize(self):
	    return {
	        'id': self.id,
            'title': self.title,
            'due_date': self.due_date.strftime(due_date_fmt),
        }


with database:
    database.create_tables([Task], safe=True)


