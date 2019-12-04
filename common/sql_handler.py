import sqlite3
import traceback
import config
config.init()


class SqlHandler:
    def __init__(self):
        self.conn = sqlite3.connect(config.db_path)

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