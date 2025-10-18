import sqlite3

from flask import Flask, request, jsonify

import models

app = Flask(__name__)

models.creates_tables()


@app.route('/')
def home():
    return "Hello Flask"


@app.route("/add_expense", methods=["POST"])
def add_expense():
    try:
        data = request.get_json()
        description = data["description"]
        category = data["category"]
        amount = data["amount"]
        date = data["date"]

        models.add_expense(description, category, amount, date)
        return jsonify({"message": "Expense added successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/get_expenses', methods=["GET"])
def get_expenses():
    rows = models.get_expense()
    expenses = [
        {
            "id": r[0],
            "description": r[1],
            "category": r[2],
            "amount": r[3],
            "date": r[4]
        }
        for r in rows
    ]
    return jsonify(expenses)


# @app.route('/delete_expense/<div>', methods=["DELETE]")
# def delete_expensive(expense_id):


if __name__ == '__main__':
    app.run(debug=True)
