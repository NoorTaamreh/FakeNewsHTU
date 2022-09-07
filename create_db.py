import sqlite3

conn = sqlite3.connect('predictions.db')

cursor = conn.cursor()

query = """CREATE TABLE PREDICTIONS(
        CREATION_TIME CHAR(26) NOT NULL,
        TEXT_BODY TEXT NOT NULL, 
        FLAG CHAR(4) NOT NULL) 
        """
cursor.execute(query)
# commit and close
conn.commit()
conn.close()