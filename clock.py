from time import monotonic
from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Digits, Button, Static
from textual.containers import Center, Middle
from pomodoro import Pomodoro, config


def format_time(seconds):
    seconds = int(seconds)
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h:02}:{m:02}:{s:02}"


class Botoes(Static):
    """ Função para organizar e colorir os botões de UI"""
    @on(Button.Pressed, "#start")
    def start_clock(self):
        self.remove_class("paused")
        self.add_class("started")

    @on(Button.Pressed, "#pause")
    def pause_clock(self):
        self.remove_class("started")
        self.add_class("paused")

    @on(Button.Pressed, "#stop")
    def stop_clock(self):
        self.remove_class("paused")
        self.remove_class("started")

    @on(Button.Pressed, "#skip")
    def skip_clock(self):
        self.remove_class("paused")
        self.add_class("started")

    def compose(self):
        yield Button("Start", variant="success", id="start")
        yield Button("Pause", variant="warning", id="pause")
        yield Button("Stop", variant="error", id="stop")
        yield Button("Skip", variant="default", id="skip")


class ClockApp(App):
    CSS_PATH = "clock.css"

    def __init__(self):
        super().__init__()
        self.pomodoro = Pomodoro(config)
        self.start_time = None
        self.timer = None
        self.elapsed_before_pause = 0

    def _start_timer(self):
        self.start_time = monotonic()
        if not self.timer:
            self.timer = self.set_interval(0.1, self.update_clock)

    def _stop_timer(self):
        if self.timer:
            self.timer.stop()
            self.timer = None
        self.start_time = None

    def _update_display(self):
        self.query_one(Digits).update(format_time(self.pomodoro.duration))

    def next_phase(self):
      self.pomodoro.next_phase()
      self.elapsed_before_pause = 0
      self.start_time = monotonic()

      self.add_class("warning")
      self.set_timer(1, lambda: self.remove_class("warning"))

      self._update_display()


    @on(Button.Pressed, "#start")
    def start_clock(self) -> None:
        self._start_timer()

    @on(Button.Pressed, "#pause")
    def pause_clock(self) -> None:
        if self.timer and self.start_time:
            self.elapsed_before_pause += monotonic() - self.start_time
            self._stop_timer()

    @on(Button.Pressed, "#stop")
    def stop_clock(self) -> None:
        self._stop_timer()
        self.elapsed_before_pause = 0
        self.pomodoro.reset()
        self._update_display()

    @on(Button.Pressed, "#skip")
    def skip_phase(self) -> None:
        self.next_phase()
        if not self.timer:
            self.timer = self.set_interval(0.1, self.update_clock)

    def update_clock(self) -> None:
        if self.start_time is None:
            return
        elapsed = self.elapsed_before_pause + (monotonic() - self.start_time)
        remaining = self.pomodoro.duration - elapsed
        if remaining <= 0:
            self.next_phase()
            return
        self.query_one(Digits).update(format_time(remaining))

    def compose(self) -> ComposeResult:
        with Middle():
            with Center():
                yield Digits(format_time(self.pomodoro.duration))
            yield Botoes()
