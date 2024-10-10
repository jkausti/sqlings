from pathlib import Path
import shutil
import duckdb
from duckdb import DuckDBPyConnection
from sqlings.exceptions import (
    SqlingsDBException,
    SqlingsProjectException,
)
from sqlings import PACKAGE_PATH


def copy_starter(project_path: Path) -> None:
    starter_path = Path(PACKAGE_PATH) / "starter"
    IGNORE_PYCACHE = "__pycache__"
    IGNORE_INIT = "__init__.py"
    IGNORE_WAL = "sqlings.duckdb.wal"
    # copy code
    try:
        shutil.copytree(
            src=starter_path,
            dst=project_path,
            ignore=shutil.ignore_patterns(IGNORE_PYCACHE, IGNORE_INIT, IGNORE_WAL),
        )
    except FileExistsError:
        raise SqlingsProjectException(
            f"Project with same name already exists in {project_path}."
        )


def get_db_connection(database_path: Path) -> duckdb.DuckDBPyConnection:

    if database_path.exists():
        try:
            con: DuckDBPyConnection = duckdb.connect(str(database_path), read_only=True)
            return con
        except Exception as e:
            raise SqlingsDBException(str(e))
    else:
        raise SqlingsDBException(f"Database {database_path} does not exist")
