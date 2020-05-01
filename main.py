import sqlite3

conn = sqlite3.connect('database.db')
cur = conn.cursor()
cur.execute("SELECT * FROM requests")
rows = cur.execute("SELECT * FROM requests")
print(rows.fetchall())
