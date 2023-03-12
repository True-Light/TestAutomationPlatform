import time
import queue

import pymysql

from typing import List

from pymysql import cursors

from core.config import settings
from core.logger import logger_server


class Connection:
    def __init__(self, is_overload: bool = False):
        """
        Mysql Connection
        :param is_overload:
        """
        self.bind_pool = None
        self.connection: pymysql.connections.Connection = pymysql.connect(
            host=settings.MYSQL_SERVER,
            port=int(settings.MYSQL_PORT),
            user=settings.MYSQL_ROOT,
            password=settings.MYSQL_ROOT_PASSWORD,
            database=settings.MYSQL_DB,
            charset="utf8mb4",
            cursorclass=cursors.DictCursor,
        )
        self.is_overload = is_overload
        self.returned = False
        self.created_at = int(time.time())

    def close(self):
        if self.bind_pool:
            self.bind_pool.put_connection(self)
        else:
            if self.connection:
                self.connection.close()
                self.connection = None

    def query_one(self, query: str, params=None):
        logger_server.debug(f"[DB] Query: {query}, params: {params}")
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            result = cursor.fetchone()
            logger_server.debug(f'[DB] Query result is: {result}')
        return result

    def query_all(self, sql: str, params=None):
        logger_server.debug(f"[DB] Query: {sql}  params: {params}")
        with self.connection.cursor() as cursor:
            cursor.execute(sql, params)
            result = cursor.fetchall()
            logger_server.debug(f'[DB] Query result: {result}')
        return result

    def query_pagination(self, sql: str, params: list, current: int = 1, page_size: int = 20):
        if page_size > 500:
            logger_server.warning(f"[DB] Up to 500 rows can be queried but {page_size}")
            page_size = 500
        sql += "LIMIT %s, %s;"
        params.extend([(current - 1) * page_size, page_size])
        return self.query_all(sql, params)

    def execute_and_commit(self, sql: str, params: dict | List[dict] | tuple | list, multiple: bool = False):
        with self.connection.cursor() as cursor:
            if multiple:
                cursor.executemany(sql, params)
            else:
                cursor.execute(sql, params)
            self.connection.commit()

    def insert(self, table_name, params: dict | List[dict]):
        if type(params) is dict:
            temp_params = params
            multiple = False
        else:
            temp_params = params[0]
            multiple = True
        columns = ", ".join(f"`{k}`" for k in temp_params.keys())
        values = ", ".join(f"%({k})s" for k in temp_params.keys())
        sql = "INSERT INTO %s (%s) VALUES (%s)" % (table_name, columns, values)
        logger_server.debug(f"[DB] Insert: {sql}, params: {params}")
        self.execute_and_commit(sql, params, multiple=multiple)


class ConnectionPool:
    """
    Return connection_pool object, which has method can get connection from a pool with timeout and retry feature;
    put a reusable connection back to the pool, etc; also we can create different instance of this class that represent
    different pool of different DB Server or different user
    """

    def __init__(
            self,
            *,
            name: str = None,
            size: int = 10,
            max_size: int = 50,
            pool_pre_ping: bool = False,
            pool_recycle: int = -1,
    ):
        """
        :param name: name of the pool
        :param size: normal size of the pool, default is 10
        :param max_size: the overflow pool size, default is 20
        :param pool_pre_ping: before use connection will ping the connection, default is False
        :param pool_recycle: the lifetime of every connection
        """
        assert max_size, "max_overflow must be greater than zero!"
        self._size = size
        self._maxsize = max_size
        self._pool = queue.Queue()
        self._pool_pre_ping = pool_pre_ping
        self._pool_recycle = pool_recycle
        self._created_num = queue.Queue()
        self.name = name if name else "Anonymous pool"

    def _create_connection(self, is_overload: bool = False):
        conn = Connection(is_overload=is_overload)
        conn.bind_pool = self
        self._created_num.put(1)
        logger_server.debug(f'Create new connection in pool({self.name})')
        return conn

    def get_connection(self) -> Connection:
        try:
            conn: Connection = self._pool.get(timeout=1)
            conn.returned = False
        except Exception as e:
            logger_server.warning(f"从连接池获取连接失败 {e}")
            if self.connection_num < self._size:
                return self._create_connection()
            else:
                if self.connection_num <= self._maxsize:
                    return self._create_connection(True)
                else:
                    raise GetConnectionFromPoolError(
                        f"can't get connection from pool{self.name}, probably should up set pool size"
                    )
        # check con_lifetime
        if 0 < self._pool_recycle <= (int(time.time()) - conn.created_at):
            conn.connection.close()
            self._created_num.get()
            logger_server.debug(f"Close connection in pool({self.name}) due to lifetime reached")
            return self._create_connection()
        else:
            if self._pool_pre_ping:
                conn.connection.ping(reconnect=True)
        logger_server.debug(f'Get connection from pool({self.name})')
        return conn

    def put_connection(self, conn):
        if conn.returned:
            logger_server.debug("Connection has been returned to pool!")
        else:
            if conn.is_overload:
                logger_server.debug("关闭超载的连接")
                conn.connection.close()
                self._created_num.get()
            else:
                logger_server.debug("将连接放入连接池")
                conn.returned = True
                self._pool.put(conn)

        logger_server.debug(f"当前mysql数据库连接池已保存的连接数为: {self.pool_size}")
        logger_server.debug(f"当前mysql数据库连接池计数为: {self.connection_num}")

    @property
    def pool_size(self):
        """available connections number for now"""
        return self._pool.qsize()

    @property
    def connection_num(self):
        return self._created_num.qsize()


class GetConnectionFromPoolError(Exception):
    """Exception related can't get connection from pool within timeout seconds."""


class ReturnConnectionToPoolError(Exception):
    """Exception related can't return connection to pool."""
