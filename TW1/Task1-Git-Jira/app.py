from flask import Flask
import psycopg2
import time

app = Flask(__name__)

while True:
    try:
        conn = psycopg2.connect(
            host="db",
            database="mydatabase",
            user="postgres",
            password="postgres"
        )
        break
    except Exception:
        print("Waiting for PostgreSQL...")
        time.sleep(2)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS messages(
    id SERIAL PRIMARY KEY,
    message TEXT
)
""")

conn.commit()

@app.route("/")
def hello():

    cursor.execute(
        "INSERT INTO messages(message) VALUES(%s)",
        ("Hello from Flask!",)
    )

    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM messages")

    count = cursor.fetchone()[0]

    return f"""
    <h1>Hello World!</h1>
    <h2>Database Connected Successfully</h2>
    <h3>Total Records: {count}</h3>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)