from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

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

@app.route('/')
def index():
    conn = sqlite3.connect('budget.db')
    cursor = conn.cursor()
    cursor.execute('SELECT SUM(amount) FROM transactions')
    balance = cursor.fetchone()[0] or 0 
    cursor.execute('SELECT * FROM transactions')
    transactions = cursor.fetchall()
    conn.close()
    return render_template('index.html', balance=balance, transactions=transactions)

@app.route('/add', methods=['POST'])
def add_transaction():
    amount = request.form['amount']
    category = request.form['category']
    description = request.form['description']
    conn = sqlite3.connect('budget.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO transactions (amount, category, description) 
    VALUES (?, ?, ?)
    ''', (amount, category, description))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db() 
    app.run(debug=True)
