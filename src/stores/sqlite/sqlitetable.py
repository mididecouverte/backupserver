class SqliteTable (object):

    def __init__(self, conn):
        self._conn = conn
        if not self.is_table_exist():
            self.create_table()
        else:
            self.update_schema()

    def reset(self):
        self.clean()
        self.create_table()

    def clean(self):
        try:
            self._conn.execute("DROP TABLE {table}".format(table=self._name))
            self._conn.commit()
        except Exception:
            pass

    def create_object(self, rec):
        obj = {}
        fields = self._get_fields()
        for i in range(len(rec)):
            obj[fields[i]] = self._create_object_field(fields[i], rec[i])
        return obj

    def _create_object_field(self, field, value):
        schema = self._get_schema()
        ftype = schema[field]['type']
        if ftype == 'bool':
            if value == 'True':
                return True
            return False
        elif ftype == 'int':
            return int(value)
        else:
            return str(value)

    def is_table_exist(self):
        try:
            r = self._conn.execute('SELECT name FROM sqlite_master where type="table" and name="{table}"'.format(table=self._name))
            return len(r.fetchall()) == 1
        except Exception:
            return False

    def create_table(self):
        self._conn.execute(self._get_create_string())
        self._conn.commit()

    def update_schema(self):
        fields = self._get_fields()
        dbfields = self._get_db_fields()
        if len(fields) != len(dbfields):
            print('Need to update schema')
            recs = self._get_alls()
            self.reset()
            for rec in recs:
                create_fields = ''
                values = ''
                for field in list(rec):
                    if field in fields:
                        create_fields += field + ','
                        values += '"' + str(rec[field]) + '",'
                create_fields = create_fields[:-1]
                values = values[:-1]
                sql = "insert into {table} ({fields}) VALUES ({values})"
                sql = sql.format(fields=create_fields, values=values, table=self._name)
                self._conn.execute(sql)
                self._conn.commit()

    def _get_fields(self):
        fields = []
        for field in self._fields:
            fields.append(field['name'])
        return fields

    def _get_schema(self):
        schema = {}
        for field in self._fields:
            schema[field['name']] = {'type': field['type'], 'default': field['default']}
        return schema

    def _get_db_fields(self):
        try:
            r = self._conn.execute('PRAGMA table_info({table})'.format(table=self._name))
            fieldsrec = r.fetchall()
            fields = []
            for rec in fieldsrec:
                fields.append(rec[1])
            return fields
        except Exception:
            return []

    def _get_create_string(self):
        sql = 'create table {table} ('.format(table=self._name)
        schema = self._get_schema()
        for field in self._get_fields():
            sql += field
            sql += ' TEXT'
            if 'default' in schema[field]:
                sql += " DEFAULT '" + str(schema[field]['default']) + "'"
            sql += ' , '
        sql = sql[:-2]
        sql += ')'
        #print(sql)
        return sql

    def _get_alls(self):
        try:
            r = self._conn.execute('select * from {table}'.format(table=self._name))
            res = r.fetchall()
            result = []
            for rec in res:
                result.append(self.create_object(rec))
            return result
        except Exception as e:
            print('get_alls', e)
            return []
