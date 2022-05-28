import unittest
import requests
import json
import sys
import datetime as dt

from task import (
    app,
    create_tables,
    DUE_DATE_FMT,
)
app.testing = True

mock_tasks = [
    {'title': 'title-1', 'due_date': '11/05/2022'},
    {'title': 'title-2', 'due_date': '12/05/2022'},
    {'title': 'title-3', 'due_date': '13/05/2022'},
    {'title': 'title-4', 'due_date': '14/05/2022'},
]

def gen_mock_tasks():
    return [{
        'title': "title_{}".format(i), 
        'due_date': dt.datetime.strftime(
            dt.datetime.now() + dt.timedelta(days=i), 
            DUE_DATE_FMT
        )
    } for i in range(1,11)]

#    '/tasks',
#    '/tasks/expire_in_days/<str:exp_day>',

#    '/task',
#    '/task/<int:id>',

class TestApp(unittest.TestCase):
    def setUp(self):
        create_tables()
#        app.run(port=5000, debug=True)
        self.mock_tasks = gen_mock_tasks()

    def test_main(self):
        with app.test_client() as client:
            res = client.post('/task', self.mock_tasks[0])
            self.assertEqual(res.data, self.mock_tasks[0])
#    def test_task_get(self):
#        res = requests.get('http://localhost:5000/task/1', )
#        self.assertEqual(res.status_code, 200)

#    def test_task_post(self):
#        res = requests.post('http://localhost:5000/task', self.mock_tasks[0])
#        self.assertEqual(res.status_code, 201)




#if __name__ == "__main__":
#    unittest.main()
