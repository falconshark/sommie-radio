import sqlite3
dbname = '../sommie.db'
conn = sqlite3.connect(dbname)
cur = conn.cursor()

cur.execute('CREATE TABLE music(id INTEGER PRIMARY KEY AUTOINCREMENT,title STRING,author STRING, file_path STRING)')
conn.commit()
conn.close()