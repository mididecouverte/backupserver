from .sqlitetable import SqliteTable


class SqliteApps(SqliteTable):

    def __init__(self, conn):
        self._name = 'apps'
        self._fields = [{'name': 'name', 'type': 'str', 'default': ''},
                        {'name': 'path', 'type': 'str', 'default': ''},
                        {'name': 'max_count', 'type': 'int', 'default': 10},
                        ]
        super().__init__(conn)

    def create(self, name, path, max_count=10):
        if not self.get(name):
            self.insert_object(name, path, max_count)

    def get_all(self):
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

    def get(self, name):
        try:
            t = (name,)
            r = self._conn.execute("select * from {table} where name=?".format(table=self._name), t)
            rec = r.fetchall()[0]
            return self.create_object(rec)
        except Exception as e:
            return None

    def update(self, name, path, max_count):
        app = self.get(name)
        if app:
            obj = (path, max_count, name, )
            try:
                sql = 'update {table} set '.format(table=self._name)
                sql += 'path=? ,'
                sql += 'max_count=?'
                sql += 'where name=?'
                self._conn.execute(sql, obj)
                self._conn.commit()
            except Exception as e:
                print('excep update', e)

    def delete(self, name):
        try:
            t = (name,)
            self._conn.execute("delete from {table} where name=?".format(table=self._name), t)
            self._conn.commit()
        except Exception:
            pass

    def insert_object(self, name, path, max_count):
        sql = "insert into {table} VALUES (".format(table=self._name)
        sql += '"' + name + '", '
        sql += '"' + path + '", '
        sql += str(max_count) + ') '
        print(sql)
        self._conn.execute(sql)
        self._conn.commit()
