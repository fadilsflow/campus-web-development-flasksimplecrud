from flask import Flask, request, render_template, flash, redirect, url_for
import pymysql

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Add a secret key for flash messages

# Database connection
# Database connection via network
def get_db_connection():
    return pymysql.connect(
        host='127.0.0.1',
        port=8889,  # Default MAMP port for MySQL
        user='root',
        password='root',
        db='flaskcru',
        cursorclass=pymysql.cursors.DictCursor
    )

# Render index.html
@app.route('/')
def index():
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM data")
        items = cursor.fetchall()
    connection.close()
    return render_template('index.html', items=items)

# Create
@app.route('/create', methods=['POST'])
def create():
    data = request.form
    connection = get_db_connection()
    with connection.cursor() as cursor:
        sql = "INSERT INTO data (name, description) VALUES (%s, %s)"
        cursor.execute(sql, (data['name'], data['description']))
    connection.commit()
    connection.close()
    flash('Record created successfully', 'success')
    return redirect(url_for('index'))

# Read
@app.route('/read', methods=['GET'])
def read():
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM data")
        result = cursor.fetchall()
    connection.close()
    return redirect(url_for('index'))

# Update
@app.route('/edit/<int:id>', methods=['GET'])
def update(id):
    connection = get_db_connection()
    with connection.cursor() as cursor:
        sql = "SELECT * FROM data WHERE id = %s"
        cursor.execute(sql, (id,))
        item =   cursor.fetchone()
    connection.close()
    if not item:
        flash('Item not found', 'danger')
        return redirect(url_for('index'))
    return render_template('update.html', item=item)

# Delete
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    connection = get_db_connection()
    with connection.cursor() as cursor:
        sql = "DELETE FROM data WHERE id = %s"
        cursor.execute(sql, (id,))
    connection.commit()
    connection.close()
    flash('Record deleted successfully', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=4000)
