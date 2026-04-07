import pyodbc
import pandas as pd
from connectors.base import BaseSource
from app.core.security import decrypt_db_password

class SQLServerConnector(BaseSource):
    def __init__(self, config):
        # Password ko decrypt karein use karne se pehle
        decrypted_pass = decrypt_db_password(config['pass'])
        self.conn_str = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={config['ip']};DATABASE={config['db']};"
            f"UID={config['user']};PWD={decrypted_pass};"
        )

    def extract_in_chunks(self, batch_size=1000):
        conn = pyodbc.connect(self.conn_str)
        query = "SELECT * FROM customers" # Future: User custom query bhi de sakta hai
        
        # Pandas use karke data ko chunks mein parhna
        for chunk in pd.read_sql(query, conn, chunksize=batch_size):
            yield chunk.to_dict(orient='records')
        
        conn.close()