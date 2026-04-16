import os
import pyodbc
from dotenv import load_dotenv


load_dotenv()


class DatabaseTrazabilidad:

    def __init__(self):
        driver_path = os.getenv(
            "DB_DRIVER_PATH",
            "/opt/homebrew/Cellar/mariadb-connector-odbc/3.2.8/lib/mariadb/libmaodbc.dylib"
        )
        server = os.getenv("DB_SERVER", "localhost")
        database = os.getenv("DB_NAME", "db_trazabilidad_alimentos")
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")

        if not user or not password:
            raise ValueError(
                "Faltan secretos de base de datos. Define DB_USER y DB_PASSWORD en .env"
            )

        self.connection_string = (
            f"DRIVER={driver_path};"
            f"SERVER={server};"
            f"DATABASE={database};"
            f"UID={user};"
            f"PWD={password};"
        )

    def get_connection(self):
        return pyodbc.connect(self.connection_string)
