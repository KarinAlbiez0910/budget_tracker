from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
db = SQLAlchemy(app)


class Expenses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    expense = db.Column(db.String(250), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(250), nullable=False)

db.create_all()

@app.route('/', methods= ['POST', 'GET'])
def add():
    if request.method == 'POST':
        date = request.form.get('date')
        expense = request.form.get('expensename')
        amount = request.form.get('amount')
        category = request.form.get('category')
        new_expense = Expenses(date=datetime.strptime(date, "%Y-%m-%d").date(),
                               expense=expense,
                               amount=amount,
                               category=category)
        db.session.add(new_expense)
        db.session.commit()
        return redirect('/expenses')
    return render_template('add.html')

@app.route('/expenses', methods= ['POST', 'GET'])
def display_expenses():
    all_expenses = db.session.query(Expenses).all()
    total = 0
    total_food = 0
    total_entertainment = 0
    total_business = 0
    total_other = 0
    for expense in all_expenses:
        total = total + expense.amount
        if expense.category == 'food':
            total_food = total_food + expense.amount
        elif expense.category == 'entertainment':
            total_entertainment = total_entertainment + expense.amount
        elif expense.category == 'business':
            total_business = total_business + expense.amount
        elif expense.category == 'other':
            total_other = total_other + expense.amount
    return render_template('expenses.html', expenses=all_expenses, total=total,
                           total_food=total_food, total_entertainment=total_entertainment,
                           total_other=total_other,total_business=total_business)

@app.route('/delete/<expense_id>', methods= ['POST', 'GET'])
def delete_expense(expense_id):
    expense_to_delete = Expenses.query.filter_by(id=expense_id).first()
    db.session.delete(expense_to_delete)
    db.session.commit()
    return redirect('/expenses')

@app.route('/update/<expense_id>', methods= ['POST', 'GET'])
def update_expense(expense_id):
    expense_to_update = Expenses.query.filter_by(id=expense_id).first()
    if request.method == 'POST':
        expense_to_update.date = datetime.strptime(request.form.get('date'), "%Y-%m-%d").date()
        expense_to_update.expense = request.form.get('expensename')
        expense_to_update.amount = request.form.get('amount')
        expense_to_update.category = request.form.get('category')
        db.session.commit()
        return redirect('/expenses')

    return render_template('update_expense.html', expense=expense_to_update)

if __name__ == '__main__':
    app.run()