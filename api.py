from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

def get_db():
    try:
        conn = sqlite3.connect('coinmarketcap.db')
        return conn
    except Exception as e:
        return None

@app.route("/rows")
def  get_rows():
    name = request.args.get('name')
    page = request.args.get('page', 1, type=int)
    per_page = 20
    offset = (page - 1) * per_page

    conn = get_db()
    if conn is None:
        return jsonify({'error': 'Database Connection failed'}), 500

    try:
        cursor = conn.cursor()
        if name:
            cursor.execute("SELECT * FROM coinmarketcap WHERE name = ? LIMIT ? OFFSET ?", (name,per_page,offset))
        else:
            cursor.execute("SELECT * FROM coinmarketcap  LIMIT ? OFFSET ?", (per_page,offset))
        columns = [desc[0] for desc in cursor.description]
        rows = [dict(zip(columns,row)) for row in cursor.fetchall()]
        return jsonify(rows)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


@app.route("/names")
def get_names():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT name FROM coinmarketcap LIMIT 20")
    rows = [row[0] for row in cursor.fetchall()]
    conn.close()
    return jsonify(rows)

if __name__ == "__main__":
    app.run(debug=True)