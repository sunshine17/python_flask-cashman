
echo "=== 1. GET : \n"
curl http://localhost:5000/task/1 -v

echo "=== 2. POST \n"
curl -X POST -H "Content-Type: application/json" -d '{
    "title": "task-1",
    "due_date": "28/05/2022"
}' http://localhost:5000/task -v


echo "=== 3. PUT \n"
curl -X PUT -H "Content-Type: application/json" -d '{
    "title": "task-1",
    "due_date": "18/03/2023"
}' http://localhost:5000/task/1 -v
