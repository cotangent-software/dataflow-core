import sqlite3

from dataflow.base import BaseNode, DataSourceNode


class DatabaseError(Exception):
    pass



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
        return {
            'name': self.resolve_input('name', env),
            'fields': fields
        }


class DatabaseObjectFieldNode(BaseNode):
    """
    Defines a field meant to be used for a database object

    Inputs
        name: The name of the field. Relational DB = column, NoSQL DB = property

        type: The type of the field. Unconnected will be interpreted as a mixed type

        required: Boolean value, true if this field should be required upon creation

    Outputs
        field: Database object field to be connected to the 'field_<n>' input of a database object
    """
    def __init__(self):
        super().__init__()

        self.declare_input('name')
        self.declare_input('type')
        self.declare_input('required')
        self.declare_output('field', self.get_output__field)

    def get_output__field(self, env):
        return {
            'name': self.resolve_input('name', env),
            'type': self.resolve_input('type', env, allow_unconnected=True, default='object'),
            'required': self.resolve_input('required', env, allow_unconnected=True, default=False)
        }


class DatabaseConnectionNode(DataSourceNode):
    def __init__(self, adapter: 'DatabaseAdapter'):
        super().__init__(adapter)


class DatabaseAdapter:
    def __init__(self):
        self.conn = None

    def connect(self):
        pass

    def disconnect(self):
        pass

    def define_object(self, schema):
        if self.conn is None:
            self.connect()

    def query(self, query_object):
        pass

    def insert(self, object_entry):
        pass

    def update(self, query_object, object_entry):
        pass

    def delete(self, query_object):
        pass


class SQLiteDatabaseAdapter(DatabaseAdapter):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename

    def connect(self):
        self.conn = sqlite3.connect(self.filename)

    def disconnect(self):
        self.conn = None

    def define_object(self, schema):
        super().define_object(schema)
        fields_str = ',\n'.join([f'{field["name"]} {self._to_sqlite_type(field["type"])}{" NOT NULL" if field["required"] else ""}' for field in schema['fields']])
        create_sql = f"""
        CREATE TABLE IF NOT EXISTS {schema['name']} (
            id INTEGER PRIMARY KEY,
{fields_str}
        );
        """
        print(create_sql)
        c = self.conn.cursor()
        c.execute(create_sql)

    def query(self, query_object):
        pass

    def insert(self, object_entry):
        pass

    def update(self, query_object, object_entry):
        pass

    def delete(self, query_object):
        pass

    @staticmethod
    def _to_sqlite_type(field_type):
        return {
            'string': 'TEXT',
            'int': 'REAL',
            'float': 'REAL',
            'array': 'TEXT',
            'dict': 'TEXT'
        }[field_type]
