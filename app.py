from flask import Flask, render_template
import psycopg2

app = Flask(__name__)

def getResults():
    postgres_conn = psycopg2.connect(
        dbname='playqueue',
        user='lemonade',
        password='supersecureadminpassword',
        host='localhost',
        port="5432",
    )
    cur = postgres_conn.cursor()
    
    cur.execute("SELECT * FROM results ORDER BY id ASC;")
    rows = cur.fetchall()
    
    cur.close()
    postgres_conn.close()
    return rows
    

@app.route('/')
def dashboard():
    rows = getResults()
    
    print(rows)
    return render_template('index.html', rows=rows)
    
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)