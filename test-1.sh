# get expenses

echo "=== 1. GET expenses: \n"
curl http://localhost:5000/expenses

# add a new expense
echo "=== 2. POST expenses \n"
curl -X POST -H "Content-Type: application/json" -d '{
    "amount": 20,
    "description": "lottery ticket"
}' http://localhost:5000/expenses

# get incomes
echo "=== 3. GET expenses: \n"
curl http://localhost:5000/incomes

# add a new income
echo "=== 4. POST income: \n"
curl -X POST -H "Content-Type: application/json" -d '{
    "amount": 300.0,
    "description": "loan payment"
}' http://localhost:5000/incomes
