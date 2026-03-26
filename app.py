from flask import Flask, render_template, request, redirect, url_for
import database

app = Flask(__name__)

database.init_db()

@app.route('/')
def index():
    conn = database.get_db_connection()
    events = conn.execute('SELECT * FROM events ORDER BY date ASC').fetchall()
    conn.close()
    return render_template('index.html', events=events)

@app.route('/add', methods=['POST'])
def add_event():
    title = request.form['title']
    date = request.form['date']
    description = request.form.get('description', '')
    
    if title and date:
        conn = database.get_db_connection()
        conn.execute('INSERT INTO events (title, date, description) VALUES (?, ?, ?)',
                     (title, date, description))
        conn.commit()
        conn.close()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_event(id):
    conn = database.get_db_connection()
    event = conn.execute('SELECT * FROM events WHERE id = ?', (id,)).fetchone()
    
    if request.method == 'POST':
        title = request.form['title']
        date = request.form['date']
        description = request.form['description']
        conn.execute('UPDATE events SET title = ?, date = ?, description = ? WHERE id = ?',
                     (title, date, description, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    conn.close()
    return render_template('edit.html', event=event)

@app.route('/delete/<int:id>')
def delete_event(id):
    conn = database.get_db_connection()
    conn.execute('DELETE FROM events WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/done/<int:id>')
def mark_done(id):
    conn = database.get_db_connection()
    conn.execute('UPDATE events SET status = CASE WHEN status = 0 THEN 1 ELSE 0 END WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)