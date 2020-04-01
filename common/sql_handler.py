import sqlite3
import traceback
import pandas as pd
from sqlalchemy import create_engine, MetaData
from sqlalchemy.pool import SingletonThreadPool
from common.log_handler import get_logger
import config
from global_values import *
config.init()
logger = get_logger()

class SqlHandler:
    def __init__(self, type='sqlite'):
        if type == 'mysql':
            logger.info("[SqlHandler Mysql init...]")
            addr = f'mysql+pymysql://{config.mysql_username}:{config.mysql_password}@{config.mysql_host}:{config.mysql_port}/{config.mysql_db}'
            self.engine = create_engine(addr, pool_size=20,
                                        max_overflow=0,
                                        pool_timeout=30)
            self.conn = self.engine.raw_connection()
        else:
            logger.info("[SqlHandler Sqlite init...]")
            self.conn = sqlite3.connect(config.db_path)
            self.engine = create_engine(f'sqlite:///{config.db_path}',
                                        poolclass=SingletonThreadPool,
                                        connect_args={'check_same_thread': True})
    
    def execute(self, sql):
        print(sql)
        try:
            logger.info(f"[SqlHandler]: execute {sql}")
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
            logger.info(f"[SqlHandler]: execute {sql}")
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
        logger.info(f"[SqlHandler]: store df to table {table}")
        data_frame.to_sql(table, self.engine, index=False, if_exists=if_exists)
        logger.info('stored into ' + table)

    def get_df(self, table=None, sql=None, chunksize=None):
        """chunksize: support to return a iterator
        """
        if table is not None:
            logger.info(f"[SqlHandler]: get from table {table}")
            return pd.read_sql(table, self.engine, chunksize=chunksize)
        elif sql is not None:
            logger.info(f"[SqlHandler]: sql {sql}")
            return pd.read_sql(sql, self.engine, chunksize=chunksize)
        else:
            raise ValueError

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
    def print_tables(self):
        tables = self.query("select name from sqlite_master where type='table';")
        for t in tables:
            sql = f"select * from sqlite_master where type='table' and name='{t[0]}'"
            res = self.query(sql)
            for item in res[0]:
                print(item)

