from time import time
from textual.events import Compose
from textual.screen import Screen
from textual.app import ComposeResult, RenderableType
from textual.containers import Container
from textual.renderables.gradient import LinearGradient
from textual.widgets import Static

COLORS = ["#008000", "#FFFF00", "#0000FF", "#FF0000", "#000000"]
STOPS = [(i / (len(COLORS) - 1), color) for i, color in enumerate(COLORS)]


class Splash(Container):
    DEFAULT_CSS: str = """
    Splash {
        align: center middle;
    }
    Static {
        width: 40;
        padding: 2 4;
    }
    """

    def on_mount(self):
        self.auto_refresh = 1 / 30

    def compose(self) -> ComposeResult:
        yield Static(
            "⭐⭐⭐\n\nCongrats!!\nYou completed Sqlings!\n\n⭐⭐⭐",
            classes="completion-text",
        )

    def render(self) -> RenderableType:
        return LinearGradient(time() * 90, STOPS)
