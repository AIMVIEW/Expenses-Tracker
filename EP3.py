import argparse
import json
from  pathlib import Path
from datetime import datetime

def load_expenses():
    file_path = Path('expenses.json')
    if file_path.exists():
        with file_path.open('r') as file:#อ่าน
            return json.load(file)
    return []

def save_expenses(expenses):
    file_path = Path('expenses.json')
    with file_path.open('w') as file:#เขียน
        json.dump(expenses, file, indent=4)

def add_expense(description, amount):
    expenses = load_expenses()
    new_id = max([expense.get('id', 0) for expense in expenses], default = 0) + 1
    expense = {
        'id': new_id,
        'date': datetime.now().strftime('%Y-%m-%d'),
        'description': description,
        'amount': amount
    }
    expenses.append(expense)
    save_expenses(expenses)
    return new_id

def main():
    parser = argparse.ArgumentParser(description='Expense Tracker')
    parser.add_argument('command', choices=['add'], help = 'Command to execute')
    parser.add_argument('--description', type = str, required=True, help='Description of expense')
    parser.add_argument('--amount', type=float, required=True, help='Amont of expense')
    args = parser.parse_args()

    if args.command == 'add':
        if args.amount <= 0:
            print('Error')
            return
        expense_id = add_expense(args.description, args.amount)
        print(f'Expense added successfully (ID: {expense_id})')

if __name__=='__main__':
    main()