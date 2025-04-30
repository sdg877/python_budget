from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Function to initialize the database and create the transactions table
def init_db():
    conn = sqlite3.connect('budget.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        description TEXT,
        date TEXT DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.commit()
    conn.close()

# Route to display balance and transactions
@app.route('/')
def index():
    conn = sqlite3.connect('budget.db')
    cursor = conn.cursor()
    cursor.execute('SELECT SUM(amount) FROM transactions')
    balance = cursor.fetchone()[0] or 0  # Default to 0 if balance is None
    cursor.execute('SELECT * FROM transactions ORDER BY date DESC')
    transactions = cursor.fetchall()
    conn.close()
    return render_template('index.html', balance=balance, transactions=transactions)

# Route to add a transaction
@app.route('/add', methods=['POST'])
def add_transaction():
    if request.method == 'POST':
        amount = float(request.form['amount'])
        category = request.form['category']
        description = request.form['description']
        transaction_type = request.form['transaction_type'].lower()

        # If it's an expense, make the amount negative
        if transaction_type == 'expense':
            amount = -abs(amount)

        # Use current time as date in database standard format
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Insert the transaction into the database with the date
        conn = sqlite3.connect('budget.db')
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO transactions (amount, category, description, date)
        VALUES (?, ?, ?, ?)
        ''', (amount, category, description, date))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

# Jinja filter to display date in UK format
@app.template_filter('datetimeformat')
def datetimeformat(value):
    try:
        dt = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        return dt.strftime('%d/%m/%Y')
    except Exception:
        return value  # fallback if parsing fails

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
