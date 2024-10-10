from pathlib import Path
from typing import Any
import tomllib


class Config:

    def __init__(self) -> None:

        self.cwd: Path = Path.cwd()
        self._project_name = self._set_project_name()

        if self._project_name:
            self._settings = self.set_settings()
            self._finished = self.read_finished()

    def _set_project_name(self) -> str | None:
        for file in self.cwd.iterdir():
            if str(file).endswith("sqlings.toml"):
                return self.cwd.parts[-1]
        else:
            return None

    @property
    def db(self) -> Path:
        return self.cwd / "sqlings.duckdb"

    @property
    def project_name(self) -> str | None:
        return self._project_name

    @project_name.setter
    def project_name(self, value: str):
        self._project_name = value

    def set_settings(self) -> dict[str, Any]:
        with open(self.cwd / "sqlings.toml", "rb") as f:
            return tomllib.load(f)

    def read_finished(self) -> tuple[str, list[str]]:
        with open(self.cwd / "finished.txt", "r") as f:
            lines = f.read().splitlines()
            return (lines[0], lines[1:])

    def update_finished(self, name: str | None = None) -> None:
        if name:
            if name not in self._finished:
                self._finished[1].append(name)
                finished_str: str = (
                    self._finished[0] + "\n" + "\n".join(self._finished[1])
                )
                with open(self.cwd / "finished.txt", "w") as f:
                    _ = f.write(finished_str)

                self._finished = self.read_finished()
            else:
                return
        else:
            finished_str: str = self._finished[0] + "\n" + "\n".join(self._finished[1])

    def remove_finished(self, name: str) -> None:
        if name in self._finished[1]:
            self._finished[1].remove(name)
            finished_str: str = self._finished[0] + "\n" + "\n".join(self._finished[1])
            with open(self.cwd / "finished.txt", "w") as f:
                _ = f.write(finished_str)

            self._finished = self.read_finished()
        else:
            return

    @property
    def finished(self) -> list[str]:
        return self._finished[1]

    @property
    def settings(self) -> dict[str, Any] | None:
        return self._settings
