from django.apps import AppConfig
from django.db.backends.signals import connection_created
from django.dispatch import receiver


class ApiConfig(AppConfig):
    name = "api"

    def ready(self):
        @receiver(connection_created)
        def set_sqlite_pragmas(sender, connection, **kwargs):
            if connection.vendor == "sqlite":
                cursor = connection.cursor()
                cursor.execute("PRAGMA journal_mode=WAL;")
                cursor.execute("PRAGMA foreign_keys=ON;")
                cursor.execute("PRAGMA synchronous=NORMAL;")
