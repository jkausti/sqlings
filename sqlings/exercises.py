from io import TextIOWrapper
import polars as pl
from polars.testing import assert_frame_equal
from duckdb import DuckDBPyConnection
from sqlings.helpers import get_db_connection
from pathlib import Path
import sqlparse
from dataclasses import dataclass
from sqlings import PACKAGE_PATH
from rich.traceback import Traceback
import sys
import os


@dataclass
class ExerciseResult:
    """Class for holding data about the result of an exercise"""

    result: bool
    traceback: tuple[str, str] | None


class Exercise:

    def __init__(self, name: str, path: Path):
        self.name: str = name
        self._path: Path = path
        self._skipped: bool = False
        self._result: ExerciseResult | None = None
        self._last_saved: float = self.get_last_saved()

    def update_save_ts(self, timestamp: float) -> None:
        self._last_saved = timestamp

    @property
    def last_saved(self) -> float:
        return self._last_saved

    def get_last_saved(self) -> float:
        timestamp = os.path.getmtime(self._path)
        return timestamp

    def analyze_result(self, db_path: Path):
        """Analyze an exercise and update _result."""
        con = get_db_connection(db_path)

        try:
            solution_df: pl.DataFrame = con.sql(self.solution_sql).pl()
            solution_df = solution_df.sort(solution_df.columns)
            exercise_df: pl.DataFrame = con.sql(self.sql).pl()
            exercise_df = exercise_df.sort(exercise_df.columns)
            con.close()
            assert_frame_equal(solution_df, exercise_df)
            self._result = ExerciseResult(result=True, traceback=None)
        except Exception:
            (exc_type, exc_value, _) = sys.exc_info()
            tb: Traceback = Traceback.from_exception(exc_type, exc_value, None)
            self._result = ExerciseResult(
                result=False,
                traceback=(tb.trace.stacks[0].exc_type, tb.trace.stacks[0].exc_value),
            )
            return

    @property
    def result(self) -> ExerciseResult | None:
        return self._result

    def get_exercise_df(self, db_path: Path) -> pl.DataFrame:
        con: DuckDBPyConnection = get_db_connection(db_path)
        try:
            exercise_df: pl.DataFrame = con.sql(self.sql).pl()
            return exercise_df
        except:
            return pl.DataFrame()

    def set_skipped(self, skipped: bool):
        self._skipped = skipped

    def _get_full_sql_text(self) -> str:
        with open(self._path, "r") as f:
            sql: str = f.read()

        return sql

    @property
    def sql(self):
        fmt_sql: str = sqlparse.format(self._get_full_sql_text(), strip_comments=True)
        return fmt_sql

    @property
    def comment(self):
        parsed: sqlparse.sql.Statement = sqlparse.parse(self._get_full_sql_text())[0]
        comment = [
            tok
            for tok in parsed.tokens
            if isinstance(tok, sqlparse.sql.Comment)
            or isinstance(tok, sqlparse.sql.Token)
        ]
        return comment[0].__str__().strip("/*\n")

    @property
    def solution_sql(self):
        """Read solution sql and return it"""

        solution_file: Path = Path(PACKAGE_PATH) / "answers" / f"{self.name}.sql"
        f: TextIOWrapper
        with open(solution_file, "r") as f:
            sql: str = f.read()

        return sql

    @property
    def skipped(self):
        return self._skipped

    def __lt__(self, other):
        """Makes class sortable based on path-value"""
        return str(self._path) < str(other._path)

    def __repr__(self):
        return f"""
Exercise name: {self.name}
Exercise path: {self.path}
Exercise skipped: {self._skipped}
Exercise result: {self._result.result if self._result is not None else ""}
Exercise last saved: {self._last_saved}
        """

    @property
    def path(self) -> str:
        if self._path:
            return str(self._path)
        else:
            return ""
