import sqlite3
import pandas as pd

class DatabaseAgent:

    def __init__(self):

        self.db_name = ':memory:'
        self.table_name = 'file_info'

        table_exists = self.table_exists()

        if table_exists:
            try:
                self.cur.execute(f"""
                CREATE TABLE {self.table_name} (
                                file_type TEXT,
                                file_sender TEXT,
                                file_subject TEXT,
                                file_intent TEXT,
                                file_urgency TEXT,
                                file_name TEXT,
                                file_size REAL
                                )
                """)
            except sqlite3.OperationalError as e:
                print('Database error',e)

        
    def table_exists(self) -> bool:
        self.conn = sqlite3.connect(self.db_name)
        self.cur = self.conn.cursor()
        self.cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{self.table_name}';")

        return self.cur.fetchone() is None
    

    def insert(self, data):
    
        metadata = data['file_metadata']
        filename = metadata['file_name']
        filesize = metadata['file_size']
        filetype = data['file_type']
        filesender = data['sender']
        filesubject = data['subject']
        fileintent = data['file_intent']
        fileurgency = data['file_urgency']
        command = f"""
                    INSERT INTO {self.table_name} (file_type,file_sender,file_subject,file_intent, 
                                                    file_urgency,file_name, file_size)
                    VALUES (?,?,?,?,?,?,?)
                    """
        try :
            self.cur.execute(command,(filetype,filesender,filesubject,fileintent,fileurgency,filename,filesize))
            self.conn.commit()

        except sqlite3.DataError as e:
            return {'DataError':e}
        
        except sqlite3.DatabaseError as e:
            return {'Database error':e}

        return 'Insertion complete!'
        

    def get_column_names(self):
        query = f"""
            PRAGMA table_info({self.table_name})
                """
        
        try :
            table_info = self.cur.execute(query)
            self.conn.commit()

        except sqlite3.DataError as e:
            return {'DataError':e}
        
        except sqlite3.DatabaseError as e:
            return {'Database error':e}

        col_names_ = [col[1] for col in table_info]

        return col_names_
    

    def fetch_data(self) -> pd.DataFrame:
        df = pd.read_sql_query(f'SELECT * FROM {self.table_name}',self.conn)
            
        return df