from .sqlitetable import SqliteTable


class SqliteBackups(SqliteTable):

    def __init__(self, conn):
        self._name = 'backup'
        self._fields = [{'name': 'app_name', 'type': 'str', 'default': ''},
                        {'name': 'date', 'type': 'str', 'default': ''},
                        {'name': 'path', 'type': 'str', 'default': ''},
                        ]
        super().__init__(conn)

    def create(self, app_name, date, path):
        if not self.get(app_name, date):
            self.insert_object(app_name, date, path)

    def get_all(self, app_name):
        try:
            r = self._conn.execute("select * from {table}".format(table=self._name))
            res = r.fetchall()
            result = []
            for rec in res:
                try:
                    result.append(self.create_object(rec))
                except Exception as e:
                    print('apps getall except', e)
            return result
        except Exception as e:
            print('apps getall except', e)
            return []

    def get(self, app_name, date):
        try:
            t = (app_name, date,)
            r = self._conn.execute("select * from {table} where app_name=? AND date=?".format(table=self._name), t)
            rec = r.fetchall()[0]
            return self.create_object(rec)
        except Exception as e:
            return None

    def delete(self, app_name, date):
        try:
            t = (app_name, date,)
            self._conn.execute("delete from {table} where name=?".format(table=self._name), t)
            self._conn.commit()
        except Exception:
            pass

    def insert_object(self, app_name, date, path):
        sql = "insert into {table} VALUES (".format(table=self._name)
        sql += '"' + app_name + '", '
        sql += '"' + date + '", '
        sql += '"' + path + '") '
        print(sql)
        self._conn.execute(sql)
        self._conn.commit()
