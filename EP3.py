import argparse
import json
from  pathlib import Path
from datetime import datetime
from tabulate import tabulate

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

def delete_expense(id):
    expenses = load_expenses()
    initial_len = len(expenses)
    expenses = [expense for expense in expenses if expense['id'] != id]
    if len(expenses) < initial_len:
        save_expenses(expenses)
        return True
    return False

def list_expenses():
    expenses = load_expenses()
    if not expenses:
        print("Not found expenses")
        return
    headers = ['ID', 'Date','Description','Amount']
    rows = [[e['id'], e['date'],e['description'],f' {e['amount']:.2f}'] for e in expenses]
    print(tabulate(rows, headers=headers, tablefmt='grid'))

def summary_expenses():
    expenses = load_expenses()
    if not expenses:
        print("Not found expenses")
        return
    total = sum(expense['amount'] for expense in expenses)
    print(f'Total expenses: {total:.2f}')

def main():
    parser = argparse.ArgumentParser(description='Expense Tracker')
    subparsers = parser.add_subparsers(dest='command', required=True)

    add_parser = subparsers.add_parser('add', help='Add a new expense')
    add_parser.add_argument('--description', type = str, required=True, help='Description of expense')
    add_parser.add_argument('--amount', type=float, required=True, help='Amont of expense')

    delete_parser = subparsers.add_parser('delete', help='Delete expense by ID')
    delete_parser.add_argument('--id', type = int, help='ID to delete')

    summary_parser = subparsers.add_parser('summary', help='summary amount')
    list_parser = subparsers.add_parser('list', help='show table each order')
    args = parser.parse_args()

    if args.command == 'add':
        if args.amount <= 0:
            print('Error')
            return
        expense_id = add_expense(args.description, args.amount)
        print(f'Expense added successfully (ID: {expense_id})')

    elif args.command == 'delete':
        if not args.id:
            print('Error: Id is required for delete')
            return
        elif delete_expense(args.id):
            print(f'Expense deleted successfully (ID: {args.id})')
        else:
            print(f'Error: Expense with ID {args.id} not found')
    elif args.command == 'list':
        list_expenses()
    elif args.command == 'summary':
        summary_expenses()

if __name__=='__main__':
    main()