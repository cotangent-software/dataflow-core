import sqlite3

from dataflow.base import BaseNode, DataSourceNode


class DatabaseError(Exception):
    pass


class ObjectField:
    def __init__(self, name, field_type, required=False, unique=False):
        self.name = name
        self.field_type = field_type
        self.required = required
        self.unique = unique

    def __str__(self):
        return self.name


class ObjectSchema:
    def __init__(self, name, fields):
        self.name = name
        self.fields = fields


class DatabaseQuery:
    def __init__(self, schema, conditions):
        self.schema = schema
        self.conditions = conditions


class DatabaseCondition:
    def __init__(self, left, right, op):
        self.left = left
        self.right = right
        self.op = op


class DatabaseObjectNode(BaseNode):
    """
    Defines a database object. In a relational database, this would be a table.
    In a NoSQL database, this would be a collection

    Inputs
        name: Name of the database object. Used in the database as a collection or document name

        field_<n>: A value which is associated with this database object

    Outputs
        db_object: Reference to a database object which can be used for database operations
    """
    def __init__(self, field_count: int = 1):
        super().__init__()

        self.field_count = field_count

        self.declare_input('name')
        for n in range(self.field_count):
            self.declare_input(f'field_{n}')
        self.declare_output('db_object', self.get_output__db_object)

    def get_output__db_object(self, env):
        fields = []
        for n in range(self.field_count):
            next_field = self.resolve_input(f'field_{n}', env, allow_unconnected=True)
            if next_field:
                fields.append(next_field)
        return ObjectSchema(
            self.resolve_input('name', env),
            fields
        )


class DatabaseObjectFieldNode(BaseNode):
    """
    Defines a field meant to be used for a database object

    Inputs
        name: The name of the field. Relational DB = column, NoSQL DB = property

        type: The type of the field. Unconnected will be interpreted as a mixed type

        required: Boolean value, true if this field should be required upon creation

        unique: Boolean value, true if this field cannot contain duplicate values

    Outputs
        field: Database object field to be connected to the 'field_<n>' input of a database object
    """
    def __init__(self):
        super().__init__()

        self.declare_input('name')
        self.declare_input('type')
        self.declare_input('required')
        self.declare_input('unique')
        self.declare_output('field', self.get_output__field)

    def get_output__field(self, env):
        return ObjectField(
            self.resolve_input('name', env),
            self.resolve_input('type', env, allow_unconnected=True, default='object'),
            self.resolve_input('required', env, allow_unconnected=True, default=False),
            self.resolve_input('unique', env, allow_unconnected=True, default=False)
        )


class DatabaseQueryNode(BaseNode):
    def __init__(self, condition_count):
        super().__init__()

        self.condition_count = condition_count

        for n in range(self.condition_count):
            self.declare_input(f'condition_{n}')
        self.declare_input('object')
        self.declare_input('db')

        self.declare_output('rows', self.get_output__rows)
        self.declare_output('query', self.get_output__query)

    def get_output__rows(self, env):
        return self.resolve_input('db', env).query(self.get_output__query(env))

    def get_output__query(self, env):
        conditions = []
        for n in range(self.condition_count):
            conditions.append(self.resolve_input(f'condition_{n}', env))
        db = self.resolve_input('db', env)
        db_object = self.resolve_input('object', env)
        db.define_object(db_object)
        return DatabaseQuery(
            db_object,
            conditions
        )


class DatabaseInsertNode(BaseNode):
    def __init__(self):
        super().__init__()

        self.declare_input('entry')
        self.declare_input('object')
        self.declare_input('db')
        self.declare_output('insert', self.get_output__insert)

    def get_output__insert(self, env):
        entry = self.resolve_input('entry', env)
        object_schema = self.resolve_input('object', env)
        db = self.resolve_input('db', env)
        db.define_object(object_schema)
        return db.insert(object_schema, entry)


class DatabaseUpdateNode(BaseNode):
    def __init__(self):
        super().__init__()

        self.declare_input('object')
        self.declare_input('query')
        self.declare_input('entry')
        self.declare_input('db')
        self.declare_output('update', self.get_output__update)

    def get_output__update(self, env):
        object_schema = self.resolve_input('object', env)
        query = self.resolve_input('query', env)
        entry = self.resolve_input('entry', env)
        db = self.resolve_input('db')
        db.define_object(object_schema)
        return db.update(object_schema, query, entry)


class DatabaseDeleteNode(BaseNode):
    def __init__(self):
        super().__init__()

        self.declare_input('object')
        self.declare_input('query')
        self.declare_input('db')
        self.declare_output('delete', self.get_input__delete)

    def get_input__delete(self, env):
        object_schema = self.resolve_input('object', env)
        query = self.resolve_input('query', env)
        db = self.resolve_input('db')
        return db.delete(object_schema, query)


class DatabaseConditionNode(BaseNode):
    def __init__(self, op='='):
        super().__init__()

        self.op = op

        self.declare_input('field')
        self.declare_input('compare')

        self.declare_output('condition', self.get_output__condition)

    def get_output__condition(self, env):
        return DatabaseCondition(
            self.resolve_input('field', env),
            self.resolve_input('compare', env),
            self.op
        )


class DatabaseConnectionNode(DataSourceNode):
    def __init__(self, adapter: 'DatabaseAdapter'):
        super().__init__(adapter)


class SQLiteDatabaseConnectionNode(DatabaseConnectionNode):
    def __init__(self, file):
        super().__init__(SQLiteDatabaseAdapter(file))


class DatabaseAdapter:
    def __init__(self):
        self.conn = None

    def connect(self):
        pass

    def disconnect(self):
        pass

    def define_object(self, schema: ObjectSchema):
        if self.conn is None:
            self.connect()

    def query(self, query_object):
        pass

    def insert(self, schema: ObjectSchema, object_entry):
        pass

    def update(self, schema: ObjectSchema, query_object: DatabaseQuery, object_entry: dict):
        pass

    def delete(self, schema: ObjectSchema, query_object: DatabaseQuery):
        pass


class SQLiteDatabaseAdapter(DatabaseAdapter):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename

    def connect(self):
        self.conn = sqlite3.connect(self.filename)

    def disconnect(self):
        self.conn = None

    def define_object(self, schema: ObjectSchema):
        super().define_object(schema)
        fields_str = ',\n'.join([f'{field.name} {self._to_sqlite_type(field.field_type)}{" NOT NULL" if field.required else ""}' for field in schema.fields])
        create_sql = f"""
        CREATE TABLE IF NOT EXISTS {schema.name} (
            id INTEGER PRIMARY KEY,
{fields_str}
        );
        """
        c = self.conn.cursor()
        c.execute(create_sql)

    def query(self, query_object: DatabaseQuery):
        c = self.conn.cursor()
        where_clause = ''
        if len(query_object.conditions) > 0:
            where_clause = self._where_clause(query_object)
        query_sql = f'SELECT * FROM {query_object.schema.name}{where_clause}'
        c.execute(query_sql)

        out = []
        rows = c.fetchall()
        for i in range(len(rows)):
            d = {}
            for j in range(len(c.description)):
                d[c.description[j][0]] = rows[i][j]
            out.append(d)
        return out

    def insert(self, schema: ObjectSchema, object_entry: dict):
        c = self.conn.cursor()
        insert_sql = f'INSERT INTO {schema.name}' \
                     f' ({",".join(object_entry.keys())}) VALUES ({",".join([self._to_sqlite_val(x) for x in object_entry.values()])}) '
        c.execute(insert_sql)
        self.conn.commit()
        c.close()

    def update(self, schema: ObjectSchema, query_object: DatabaseQuery, object_entry: dict):
        c = self.conn.cursor()

        entry_defs = ','.join([x[0] + ' = ' + self._to_sqlite_val(x[1]) for x in zip(object_entry.keys(), object_entry.values())])

        update_sql = f'UPDATE {schema.name} SET {entry_defs} {self._where_clause(query_object)}'
        c.execute(update_sql)
        self.conn.commit()
        c.close()

    def delete(self, schema: ObjectSchema, query_object: DatabaseQuery):
        c = self.conn.cursor()

        delete_sql = f'DELETE FROM {schema.name} {self._where_clause(query_object)}'
        c.execute(delete_sql)
        self.conn.commit()
        c.close()

    @staticmethod
    def _to_sqlite_type(field_type):
        return {
            'string': 'TEXT',
            'int': 'REAL',
            'float': 'REAL',
            'array': 'TEXT',
            'dict': 'TEXT'
        }[field_type]

    @staticmethod
    def _to_sqlite_val(field_value):
        t = type(field_value)
        if t == str:
            return "'" + field_value.replace("'", "\'") + "'"
        return str(field_value)

    @staticmethod
    def _where_clause(query_object):
        return ' WHERE ' + ' AND '.join([str(x.left) + x.op + SQLiteDatabaseAdapter._to_sqlite_val(x.right) for x in query_object.conditions])


BaseNode.NodeRegistry.extend([
    DatabaseObjectNode,
    DatabaseObjectFieldNode,
    DatabaseQueryNode,
    DatabaseInsertNode,
    DatabaseConnectionNode,
    SQLiteDatabaseConnectionNode
])
