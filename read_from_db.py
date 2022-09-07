import sqlite3
conn = sqlite3.connect('predictions.db')
cursor = conn.execute("SELECT * from PREDICTIONS")
print(cursor.fetchall())
conn.close()