# get expenses

echo "=== 1. GET expenses: \n"
curl http://localhost:5000/task/1

# add a new expense
echo "=== 2. POST expenses \n"
curl -X POST -H "Content-Type: application/json" -d '{
    "title": "task-1",
    "due_date": "2022-05-27 16:33:40"
}' http://localhost:5000/task
