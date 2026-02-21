import tomllib

with open("pomodoro.toml", "rb") as f:
    config = tomllib.load(f)

PHASE_NAMES = {
    "focus": "Foco",
    "break": "Pausa",
    "long_break": "Pausa Longa",
}


class Pomodoro:
    def __init__(self, config):
        self.focus = config["phases"]["focus_duration"]
        self.break_ = config["phases"]["break_duration"]
        self.long_break = config["phases"]["long_break_duration"]
        self.cycles_before_long = config["phases"]["cycles_before_long_break"]

        self.current_phase = "focus"
        self.cycles_done = 0

    def next_phase(self):
        if self.current_phase == "focus":
            self.cycles_done += 1
            if self.cycles_done % self.cycles_before_long == 0:
                self.current_phase = "long_break"
            else:
                self.current_phase = "break"
        else:
            self.current_phase = "focus"

    def reset(self):
        self.current_phase = "focus"
        self.cycles_done = 0

    @property
    def duration(self):
        return {
            "focus": self.focus,
            "break": self.break_,
            "long_break": self.long_break,
        }[self.current_phase]

    @property
    def phase_name(self):
        return PHASE_NAMES[self.current_phase]
