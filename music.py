import sqlite3

def loadMusicList():
    conn = sqlite3.connect('sommie.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM music')
    print(cur.fetchall())
    cur.close()
    conn.close()