import sqlite3
import traceback
import pandas as pd
from sqlalchemy import create_engine, MetaData
from common.log_handler import get_logger
import config
from global_values import *
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

    def df_to_db(self, data_frame, table, if_exists):
        """if_exists: 'append' or 'replace'
        """
        data_frame.to_sql(table, self.engine, index=False, if_exists=if_exists)
        logger.info('stored into ' + table)

    def get_df(self, table):
        return pd.read_sql(table, self.engine)

    def get_cloumns_from_table(self, table):
        if type(table) == str:
            df = pd.read_sql(f'select * from {table} limit 1', self.engine)
            return list(df.columns.values)
        else:
            audio_fea, video_fea, text_fea = [], [], []
            for tb in table:
                df = pd.read_sql(f'select * from {table} limit 1', self.engine)
                cols = df.columns.values
                if tb in AUDIO_TABLE:
                    audio_fea += cols
                elif tb in VIDEO_TABLE:
                    video_fea += cols
                elif tb in TEXT_TABLE:
                    text_fea += cols
                else:
                    raise ValueError
            