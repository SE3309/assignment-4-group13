import string
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Database connection configuration
db_config = {
    'host': 'localhost',
    'user': 'root',  # Your MySQL username
    'password': 'Ans19122004',  # Your MySQL password
    'database': 'expensetracker'
}

# Function to connect to MySQL database
def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        try:
            # Handle form submission
            category = request.form['category']
            date = request.form['date']
            expense_paid = request.form['expense_paid']
            total_expense = request.form['total_expense']
            user_id = request.form['user_id']

            # Log the form data for debugging
            print(f"Category: {category}, Date: {date}, Paid: {expense_paid}, Total: {total_expense}, UserID: {user_id}")

            connection = get_db_connection()
            cursor = connection.cursor()

            # Insert data into the expense table
            cursor.execute('''INSERT INTO expense (ExpenseCategory, DateOfExpense, ExpensePaid, TotalExpense, UserID)
                              VALUES (%s, %s, %s, %s, %s)''',
                           (category, date, expense_paid, total_expense, user_id))

            connection.commit()
            cursor.close()
            connection.close()

            return redirect(url_for('view_expenses'))
        
        except mysql.connector.Error as err:
            # Log the error and display it
            print(f"Error: {err}")
            return f"Error: {err}"

    return render_template('add_expense.html')



@app.route('/view_income')
def view_income():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute('SELECT * FROM income')
    incomes = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('view_income.html', incomes=incomes)

# More routes for other tables like transactions, reports, etc. as required

if __name__ == '__main__':
    app.run(debug=True)
