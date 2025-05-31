import sqlite3

conn = sqlite3.connect('file.db')
cur = conn.cursor()

query = """
    DROP TABLE file_info
"""

cur.execute(query)
conn.commit()
conn.close