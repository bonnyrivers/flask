import sqlite3


conn = sqlite3.connect('database.db')

with open('schema.sql') as f:
    conn.executescript(f.read())

cur = conn.cursor()

cur.execute("INSERT INTO posts (title,content) VALUES (?,?)",
    ('First Post', 'Content for the first post')
)

conn.commit()
conn.close()