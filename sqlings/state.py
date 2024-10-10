from sqlings.exceptions import SqlingsProjectException
from sqlings.exercises import Exercise, ExerciseResult
from sqlings.config import Config
from pathlib import Path
import os
import datetime
from rich.table import Table


class AppState:

    def __init__(self, config: Config):
        self.config: Config = config
        self._exercises: list[Exercise] = self._get_exercises()
        self.refresh()
        self._next_exercise: Exercise = self.get_next_exercise()

    def refresh(self):
        """Update status of exercises for files that have been saved again"""

        ex: Exercise
        for ex in self._exercises:

            ts_fs: float = os.path.getmtime(ex.path)
            ex.analyze_result(self.config.db)

            if ts_fs != ex.last_saved:
                ex.update_save_ts(ts_fs)
                self._next_exercise = self.get_next_exercise()
            else:
                continue

    def get_next_exercise(self) -> Exercise:
        """Sets what the next exercise to solve is"""

        ex: Exercise
        for ex in self._exercises:
            if len(self.config.finished) == 0:
                return ex
            elif (
                isinstance(ex.result, ExerciseResult)
                and ex.result.result == True
                and ex.name not in self.config.finished
            ):
                return ex
            elif (
                isinstance(ex.result, ExerciseResult)
                and ex.result.result == False
                and ex.name in self.config.finished
            ):
                self.config.remove_finished(ex.name)
                return ex
            elif (
                isinstance(ex.result, ExerciseResult)
                and ex.result.result == False
                and ex.name not in self.config.finished
            ):
                return ex
            elif (
                isinstance(ex.result, ExerciseResult)
                and ex.result.result == True
                and ex.name in self.config.finished
            ):
                continue

        else:
            return self._exercises[-1]

    def update_next_exercise(self):
        self._next_exercise = self.get_next_exercise()

    @property
    def next_exercise(self) -> Exercise:
        """Getter for next exercise"""
        return self._next_exercise

    def _get_exercises(self) -> list[Exercise]:
        """Reads exercises from file system and returns as exercise objects"""
        if self.config.project_name:
            paths: list[Path] = list(self.config.cwd.glob("exercises/*/*.sql"))

            ex_list: list[Exercise] = [Exercise(p.stem, path=p) for p in paths]
            ex_list.sort()

            return ex_list
        else:
            raise SqlingsProjectException(
                "Command can only be run from inside a valid Sqlings project."
            )

    def get_exercises(self) -> list[Exercise]:
        return self._exercises

    @property
    def table(self) -> Table:

        table: Table = Table(title="Exercises")
        row: list[str] = []

        ex: Exercise
        for ex in self._exercises:
            table.add_column(ex.name)

            if ex.result.result:
                row.append("\N{Check Mark}")
            else:
                row.append("\N{Cross Mark}")

        table.add_row(*row)
        return table
