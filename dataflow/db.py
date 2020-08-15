from dataflow.base import BaseNode, DataSourceNode, GraphError
import sqlite3


class DatabaseNode(BaseNode):
    def __init__(self, conn):
        super().__init__()

        self.conn = conn

        self.declare_output('conn', self.get_output__conn)

    def get_output__conn(self, env):
        return self.conn


class DatabaseQueryNode(BaseNode):
    def __init__(self, query):
        super().__init__()

        self.query = query

        self.declare_input('conn')
        self.declare_input('variables')
        self.declare_output('meta', self.get_output__meta)
        self.declare_output('data', self.get_output__data)

    def get_output__meta(self, env):
        raise GraphError('DatabaseQueryNode meta output unimplemented')

    def get_output__data(self, env):
        raise GraphError('DatabaseQueryNode data output unimplemented')


class SQLiteDatabaseNode(DatabaseNode):
    def __init__(self, db_file):
        conn = sqlite3.connect(db_file)
        super().__init__(conn)


class SQLiteQueryNode(DatabaseQueryNode):
    def __init__(self, query):
        super().__init__(query)

    def get_output__meta(self, env):
        self.get_output__data(env)
        return self.output_cache['meta']

    def get_output__data(self, env):
        if 'data' in self.output_cache:
            return self.output_cache['data']

        conn = self.resolve_input('conn')
        cur = conn.cursor()
        cur.execute(self.query, tuple(self.resolve_input('variables')))

        rows = cur.fetchall()
        self.cache_output('data', rows)
        self.cache_output('meta', {
            'rowcount': cur.rowcount,
            'lastrowid': cur.lastrowid,
            'arraysize': cur.arraysize,
            'description': cur.description
        })

        return rows


# class MongoDatabaseNode(DatabaseNode):
#     def __init__(self, uri):
#         super().__init__()


# class MongoQueryNode(DatabaseQueryNode):
#     def __init__(self, query):
#         super().__init__(query)

BaseNode.NodeRegistry.extend([
    SQLiteDatabaseNode,
    SQLiteQueryNode
])
