
from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2  # pip install psycopg2
import psycopg2.extras

main = Flask(__name__)
main.secret_key = "malika"

DB_HOST = "localhost"
DB_NAME = "hw"
DB_USER = "postgres"
DB_PASS = "1234"

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

@main.route('/')
def Index():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "SELECT * FROM users"
    cur.execute(s)  # Execute the SQL
    list_users = cur.fetchall()
    return render_template('index.html', list_users=list_users)


@main.route('/add', methods=['POST'])
def add():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        cur.execute("INSERT INTO users (name, surname, email) VALUES (%s,%s,%s)", (name, surname, email))
        conn.commit()
        flash('User Added successfully')
        return redirect(url_for('Index'))


@main.route('/edit/<email>', methods=['POST', 'GET'])
def get_employee(email):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute('SELECT * FROM users', (email))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit.html', user=data[0])


@main.route('/update/<email>', methods=['POST'])
def update(email):
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']

        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("""
            UPDATE users
            SET name = %s,
                surname = %s,
                email = %s
            WHERE email = %s
        """, (name, surname, email, email))
        flash('Information Updated Successfully')
        conn.commit()
        return redirect(url_for('Index'))


@main.route('/delete/<email>', methods=['POST', 'GET'])
def delete_user(email):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute("""
            DELETE FROM users
            WHERE email LIKE %s
        """, [email])
    conn.commit()
    flash('Removed Successfully')
    return redirect(url_for('Index'))

if __name__ == "__main__":
    main.run(debug=True)
