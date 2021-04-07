from pymysql import connect, converters
from pymysql.cursors import DictCursor


class DB:

    HOST = None
    USER = None
    PASSWORD = None
    DATABASE = None
    PORT = None
    conn_name = None
    _connection = None
    _cursor = None
    _last_query = None

    def __init__(self, host=None, user=None, password=None, database=None, port=None, conn_name=None):
        self.HOST = host
        self.USER = user
        self.PASSWORD = password
        self.DATABASE = database
        self.PORT = port
        self.conn_name = conn_name
        self._connect()

    def show_all(self):
        print(f'{self.HOST}, {self.USER}, {self.PASSWORD}, {self.PORT}')

    def _connect(self):
        result = False

        try:
            self._connection = connect(host=self.HOST, user=self.USER, password=self.PASSWORD, database=self.DATABASE,
                                       charset='utf8mb4', port=int(self.PORT), cursorclass=DictCursor)
            self._cursor = self._connection.cursor()
        except Exception as e:
            print(f'_connect: {e}')
            exit(0)
        else:
            result = True

        return result

    def get_connection(self):
        return self._connection

    def get_cursor(self):
        return self._cursor

    def execute(self, query=None):

        self._last_query = converters.escape_str(query)
        try:
            self._cursor.execute(query=query)
        except Exception as e:
            print(f'Execution error: {e}')
            # exit(0)
        else:
            return True

    def commit(self):
        pass

    def close(self):
        self._cursor.close()
        self._connection.close()

