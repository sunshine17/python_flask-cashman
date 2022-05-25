from flask import Flask, jsonify, request
from flask_restful import Resource, Api

from cashman.model.expense import Expense, ExpenseSchema
from cashman.model.income import Income, IncomeSchema
from cashman.model.transaction_type import TransactionType

app = Flask(__name__)
api = Api(app)

transactions = [
  Income('Salary', 5000),
  Income('Dividends', 200),
  Expense('pizza', 50),
  Expense('Rock Concert', 100)
]


class Incomes(Resource):

    def get(self):
        schema = IncomeSchema(many=True)
        incomes = schema.dump(
            filter(lambda t: t.type == TransactionType.INCOME, transactions)
        )
        return jsonify(incomes)

    def post(self):
        income = IncomeSchema().load(request.get_json())
        transactions.append(income)
        return "", 204

class Expenses(Resource):

    def get(self):
        schema = ExpenseSchema(many=True)
        expenses = schema.dump(
            filter(lambda t: t.type == TransactionType.EXPENSE, transactions)
        )
        return jsonify(expenses)

    def post(self):
        expense = ExpenseSchema().load(request.get_json())
        transactions.append(expense)
        return "", 204

api.add_resource(Incomes, '/incomes')
api.add_resource(Expenses, '/expenses')


if __name__ == "__main__":
    app.run(debug=True)
