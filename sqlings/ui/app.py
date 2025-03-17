from textual.containers import Container
from sqlings.state import AppState
from textual.app import App
from textual.binding import Binding
from textual.widgets import Footer, Static, DataTable
from sqlings.ui import CURRENT_DIR
from pathlib import Path
from sqlings.config import Config
from sqlings.ui.splash import Splash

import polars as pl
import os


class ResultTable(DataTable):

    def set_data(self, df: pl.DataFrame):
        columns = [col for col, _ in df.schema.items()]
        rows = df.select(pl.all()).limit(5).rows()

        self.add_columns(*columns)
        self.add_rows(rows)


class SqlingsApp(App):

    CSS_PATH: str = str(Path(CURRENT_DIR) / "sqlings.tcss")

    BINDINGS: list[Binding] = [
        Binding(
            key="q",
            action="quit",
            description="Exit app",
        ),
        Binding(
            key="n",
            action="goto_next",
            description="Go to next exercise",
            show=False,
        ),
    ]

    def __init__(self, state: AppState, config: Config):
        self.state: AppState = state
        self.config = config
        super().__init__()

    def compose(self):

        result_table = ResultTable(classes="result-table")
        curr_ex_df = self.state.next_exercise.get_exercise_df(self.config.db)
        result_table.set_data(curr_ex_df)

        all_done = False
        exercise_results = [
            ex.result.result
            for ex in self.state.get_exercises()
            if not ex.result.result
        ]
        if not exercise_results:
            yield Splash()
        else:
            with Container(classes="container1") as c:
                c.border_title = f"Current exercise - {self.state.next_exercise.name}"
                yield Static(
                    self.state.next_exercise.path,
                    classes="text1",
                    markup=False,
                )

            with Container(classes="container1") as c:
                c.border_title = "Exercise description"
                yield Static(
                    str(self.state.next_exercise.comment),
                    classes="text1",
                    markup=False,
                )

            with Container(classes="container1") as c:
                c.border_title = "Data Preview"
                if result_table.rows:
                    yield result_table
                else:
                    yield Static("Could not run query.")

            if self.state.next_exercise.result.result:
                with Container(classes="success-result-container") as c4:
                    c4.border_title = "Result"
                    yield Static(
                        "Congrats! You solved the exercise!", classes="success-text"
                    )

                yield Static("Press n to go to next exercise!", classes="goto-next")

            else:
                with Container(classes="error-result-container") as c5:
                    c5.border_title = "Result"
                    yield Static(
                        self.state.next_exercise.result.traceback[1],
                        classes="error-text",
                        markup=False,
                    )

            yield Footer()

    def on_mount(self) -> None:
        self.title = "Sqlings"
        _ = self.set_interval(1, self.monitor_project)

    async def monitor_project(self):

        ex_list = self.state.get_exercises()
        new_saved_times = [(os.path.getmtime(ex.path), ex) for ex in ex_list]

        for save_time, ex in new_saved_times:
            if save_time > ex.last_saved:
                self.state.refresh()
                await self.recompose()

    async def action_goto_next(self):
        if self.state.next_exercise.result.result:
            self.config.update_finished(self.state.next_exercise.name)
            self.state.update_next_exercise()
            await self.recompose()
        else:
            pass
