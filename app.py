from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB = 'reposteria.db'

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS pedidos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente TEXT NOT NULL,
                producto TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                fecha_entrega TEXT NOT NULL,
                estado TEXT DEFAULT 'pendiente'
            )
        ''')
        conn.commit()

@app.route('/')
def index():
    conn = get_db()
    pedidos = conn.execute('SELECT * FROM pedidos ORDER BY fecha_entrega').fetchall()
    conn.close()
    return render_template('index.html', pedidos=pedidos)

@app.route('/agregar', methods=['POST'])
def agregar():
    cliente = request.form['cliente']
    producto = request.form['producto']
    cantidad = request.form['cantidad']
    fecha_entrega = request.form['fecha_entrega']
    with get_db() as conn:
        conn.execute('INSERT INTO pedidos (cliente, producto, cantidad, fecha_entrega) VALUES (?, ?, ?, ?)',
                     (cliente, producto, cantidad, fecha_entrega))
        conn.commit()
    return redirect(url_for('index'))

@app.route('/entregar/<int:id>')
def entregar(id):
    with get_db() as conn:
        conn.execute("UPDATE pedidos SET estado='entregado' WHERE id=?", (id,))
        conn.commit()
    return redirect(url_for('index'))

@app.route('/eliminar/<int:id>')
def eliminar(id):
    with get_db() as conn:
        conn.execute('DELETE FROM pedidos WHERE id=?', (id,))
        conn.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
