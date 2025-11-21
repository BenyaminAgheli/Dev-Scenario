from flask import Flask, request, jsonify
import mysql.connector
import os

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "mysql"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASS", "root"),
        database=os.getenv("DB_NAME", "testdb")
    )

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
