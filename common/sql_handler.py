import sqlite3
import traceback
import pandas as pd
from sqlalchemy import create_engine, MetaData
from common.log_handler import get_logger
import config
config.init()

logger = get_logger()

class SqlHandler:
    def __init__(self):
        self.conn = sqlite3.connect(config.db_path)
        self.engine = create_engine(f'sqlite:///{config.db_path}')
    
    def execute(self, sql):
        try:
            cur = self.conn.cursor()
            cur.execute(sql)
            res = None
            if 'returning' in sql:
                res = cur.fetchone()
            self.conn.commit()
            cur.close()
            return res
        except:
            traceback.print_exc()

    def query(self, sql):
        try:
            cur = self.conn.cursor()
            cur.execute(sql)
            res = cur.fetchall()
            cur.close()
            if not res:
                res = []
            return res
        except:
            traceback.print_exc()
            return

    def disconnect(self):
        """Always remember to invoke disconnect
        """
        self.conn.close()
        return

    def df_to_db(self, data_frame, table):
        data_frame.to_sql(table, self.engine, index=False)
        logger.info('stored into ' + table)

    def get_df(self, table):
        return pd.read_sql(table, self.engine)