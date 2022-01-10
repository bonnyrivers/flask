import sqlite3
from flask import Flask, request, render_template, abort, url_for, flash, redirect

app = Flask(__name__)

def get_db_connection():
	conn = sqlite3.connect('database.db')
	conn.row_factory = sqlite3.Row
	return conn

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

@app.route('/')
@app.route('/index/')
def index():
	conn = get_db_connection()
	posts = conn.execute('SELECT * FROM posts').fetchall()
	return render_template('index.html', posts=posts)

@app.route('/hello/')
def hello():
	return '<h1>Hello, world!</h1>'

@app.route('/about/')
def about():
	return '<h3>This is a flask web app</h3>'

@app.route('/create/', methods=('GET', 'POST'))
def create():
	if request.method == 'POST':
		title = request.form['title']
		content = request.form['content']
	if not title:
		flash('Title is required')
	elif not content:
		flash('Content is required')
	else:
		conn = get_db_connection()
		conn.execute('INSERT INTO posts (title, content) VALUE (?,?)',
			(title, content)
		)
		conn.commit()
		conn.close()
		return redirect(url_for('index'))

	return render_template('create_form.html')
