import sqlite3
from .sqliteapps import SqliteApps
from .sqlitebackups import SqliteBackups

class SqliteStore():

    def __init__(self, db='backupds.db'):
        self._db = db
        self._conn = sqlite3.connect(self._db)
        self.apps = SqliteApps(self._conn)
        self.backups = SqliteBackups(self._conn)

    def reset(self):
        self.apps.reset()
        self.backups.reset()

    def clean(self):
        self.apps.clean()
        self.backups.clean()

    def open(self):
        self._conn = sqlite3.connect(self._db)
        self.apps._conn = self._conn
        self.backups._conn = self._conn

    def close(self):
        self._conn.close()
