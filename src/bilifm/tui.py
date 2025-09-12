from textual.app import App, ComposeResult
from textual.color import Gradient
from textual.containers import Center, Middle, VerticalScroll
from textual.widgets import Button, Digits, Footer, Header, ProgressBar


class ProgressApp(App[None]):
    """Progress bar with a rainbow gradient."""

    BINDINGS = [("q", "exit", "Exit the application")]

    def compose(self) -> ComposeResult:
        gradient = Gradient.from_colors(
            "#881177",
            "#aa3355",
            "#cc6666",
            "#ee9944",
            "#eedd00",
            "#99dd55",
            "#44dd88",
            "#22ccbb",
            "#00bbcc",
            "#0099cc",
            "#3366bb",
            "#663399",
        )

        yield Header()
        yield Footer()

        with Center():
            with Middle():
                yield ProgressBar(total=100, gradient=gradient)

    def on_mount(self) -> None:
        self.query_one(ProgressBar).update(progress=70, total=200)

    def action_exit(self) -> None:
        self.exit()


def run_tui():
    app = ProgressApp()
    app.run()


if __name__ == "__main__":
    run_tui()
