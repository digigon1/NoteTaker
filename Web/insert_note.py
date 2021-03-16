import sqlite3

con = sqlite3.connect('files.db', check_same_thread=False)
cur = con.cursor()
cur.execute('insert into notes (title) values ("test")')
con.commit()
