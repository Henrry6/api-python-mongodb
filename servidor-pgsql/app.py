from psycopg2 import extras
# from dotenv import load_dotenv
from database.db import get_connection
from flask import Flask, request, jsonify

# load_dotenv()  # loads variables from .env file into environment

app = Flask(__name__)

CREATE_USER_TABLE = (
    "CREATE TABLE IF NOT EXISTS users(id SERIAL PRIMARY KEY, username TEXT, password CHARACTER(6), email CHARACTER(50))"
)
INSERT_USER_TABLE = (
    "INSERT INTO users (username, password, email) VALUES(%s, %s, %s) RETURNING *;"
)


@app.post("/users")
def create_user():
    user = request.get_json()
    username = user['username']
    password = user['password']
    email = user['email']
    conecction = get_connection()
    with conecction.cursor(cursor_factory=extras.RealDictCursor) as cursor:
        cursor.execute(CREATE_USER_TABLE)
        cursor.execute(INSERT_USER_TABLE, (username, password, email))
        user_created = jsonify(cursor.fetchone())
        # al finalizar
        conecction.commit()
        cursor.close()
        conecction.close()
    return user_created


@app.get('/users')
def get_users():
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(users)


@app.get('/users/<id>')
def get_user(id):
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
    cursor.execute('SELECT * FROM users WHERE id = %s', (id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if user is None:
        return jsonify({'message': 'User not found'}), 404
    return jsonify(user)


@app.delete('/users/<id>')
def delete_user(id):
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
    cursor.execute('DELETE FROM users WHERE id = %s RETURNING *', (id,))
    user = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    if user is None:
        return jsonify({'message': 'User not found'}), 404
    return jsonify(user)


@app.put('/users/<id>')
def put_user(id):
    user = request.get_json()
    username = user['username']
    password = user['password']
    email = user['email']
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
    cursor.execute('UPDATE users SET username = %s, email = %s, password = %s WHERE id = %s RETURNING *',
                   (username, email, password, id))
    user_updated = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    if user_updated is None:
        return jsonify({'message': 'User not found'}), 404
    return jsonify(user_updated)


if __name__ == "__main__":
    app.run(debug=True)
