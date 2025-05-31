import sqlite3
import pandas as pd

conn = sqlite3.connect('file.db')
cur = conn.cursor()

command = """
    SELECT * FROM file_info
"""
command2 = """
    PRAGMA table_info(file_info)
"""
table_info = cur.execute(command).fetchall()
conn.commit()
table_col = cur.execute(command2).fetchall()
conn.commit()


column_names = [col[1] for col in table_col]
data = table_info

df = pd.DataFrame(data=data,columns=column_names)
print(df.iloc[-1])


conn.close()