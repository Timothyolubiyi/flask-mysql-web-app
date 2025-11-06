import os

from flask import Flask, render_template, request, redirect, url_for
#from flask_mysqldb import MySQL
#from flaskext.mysql import MySQL
from dotenv import load_dotenv
load_dotenv()

from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)

# Configure MySQL from environment variables
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'MYSQL_HOST')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', 'MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'MYSQL_DB')

# Initialize MySQL
mysql = MySQL(app)

# Create 'messages' table if it doesn't exist
with app.app_context():
    cur = mysql.connection.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INT AUTO_INCREMENT PRIMARY KEY,
            message TEXT
        )
    ''')
    mysql.connection.commit()
    cur.close()

@app.route('/')
def hello():
    cur = mysql.connection.cursor()
    cur.execute('SELECT message FROM messages')
    post = cur.fetchall()
    cur.close()
    if post:
        return render_template('index.html', posts=post)
    return render_template('nomessage.html')

@app.route('/submit', methods=['POST'])
def submit():
    new_message = request.form.get('new_message')
    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO messages (message) VALUES (%s)', [new_message])
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('hello'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2000, debug=True)
