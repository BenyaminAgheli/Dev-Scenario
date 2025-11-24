from flask import Flask, request, jsonify
import mysql.connector
import os

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "mysql"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASS", "root"),
        database=os.getenv("DB_NAME", "testdb")
    )


def create_table():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
	    email VARCHAR(255) NOT NULL
        );
    """)
    conn.commit()
    conn.close()


app = Flask(__name__)

create_table()

@app.route("/users", methods=["GET"])
def users():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, name, email FROM users")
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify({"users": data})

@app.route("/health", methods=["GET"])
def health():
    print("test pipline")
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
