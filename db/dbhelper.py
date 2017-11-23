import MySQLdb
import sys
sys.path.append("../../FCS/")
    
from utils.loghelper import PBSLogger
from utils.singleton import Singleton
from pool import PooledDB

class DataDriver(object): pass
#
#     def select(self, data):
#         return None
#
#     def update(self, data):
#         return None
#
#     def delete(self, data):
#         return None

class MysqlDriver(DataDriver):

    def __init__(self, **kwargs):
        self._host = kwargs.get('host', 'localhost')
        self._db = kwargs.get('db', 'test_db')
        self._user = kwargs.get('user', 'root')
        self._passwd = kwargs.get('passwd', '')
        self._port = kwargs.get('port', 3306)
        self._logger = PBSLogger.getLogger('mysql')

    def query(self, sql, get_one=False):
        conn = None
        cur = None
        try:
            sql = sql.encode('utf8')
            conn = self.create_connection()
            cur = conn.cursor(MySQLdb.cursors.DictCursor)
            count = cur.execute(sql)
            if count == 0:
                return []
            if get_one:
                result = cur.fetchone()
            else:
                result = cur.fetchall()
            return result
        except:
            self._logger.exception(sql)
        finally:
            if cur is not None:
                try:
                    cur.close()
                except:
                    pass
            if conn is not None:
                try:
                    conn.close()
                except:
                    pass

    def execute(self, *sqls):
        cur = None
        conn = None
        try:
            conn = self.create_connection()
            cur = conn.cursor()
            cur.execute('set names utf8;')
            for sql in sqls:
                sql = sql.encode('utf8')
                cur.execute(sql)
            lastid = cur.lastrowid
            conn.commit()
            return lastid
        except:
            self._logger.exception(sqls)
        finally:
            if cur is not None:
                try:
                    cur.close()
                except:
                    pass
            if conn is not None:
                try:
                    conn.close()
                except:
                    pass

        return 0

    def create_connection(self):
        conn = MySQLdb.connect(host=self._host, user=self._user, passwd=self._passwd, db=self._db)
        conn.set_character_set('utf8')
        return conn


class PooledMysqlDriver(MysqlDriver):

    def __init__(self, **kwargs):
        super(PooledMysqlDriver, self).__init__(**kwargs)
        self._pool = PooledDB(creator=MySQLdb,
                              mincached=10,
                              maxcached=100,
                              host=self._host,
                              user=self._user,
                              passwd=self._passwd,
                              db=self._db,
                              port=self._port)

    def create_connection(self):
        return self._pool.connection()

class DriverProxy:

    __metaclass__ = Singleton

    def __init__(self):
        self._driver = PooledMysqlDriver(host='127.0.0.1', db='facedb', user='root', passwd='root')

    def query(self, sql, get_one=False):
        return self._driver.query(sql, get_one)

    def execute(self, *sqls):
        return self._driver.execute(*sqls)

class PooledDriverProxy:

    __metaclass__ = Singleton

class DBHelper:

    @staticmethod
    def query(sql, get_one=False):
        return DriverProxy().query(sql, get_one)

    @staticmethod
    def execute(*sqls):
        return DriverProxy().execute(*sqls)

if __name__ == '__main__':
    res = DBHelper.query('select * from image')
    print res