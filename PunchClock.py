from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from datetime import datetime


class PunchClock(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.times = {}
        display = Label(text="Punch Clock")
        self.ids["display"] = display
        self.add_widget(display)

        button_layout = BoxLayout(orientation="horizontal")

        punch_in = Button(text="Punch In")
        punch_in.bind(on_press=self.punch_in)
        self.ids["punch_in"] = punch_in

        lunch_start = Button(text="Start Lunch", disabled=True)
        lunch_start.bind(on_press=self.lunch_start)
        self.ids["lunch_start"] = lunch_start

        lunch_end = Button(text="End Lunch", disabled=True)
        lunch_end.bind(on_press=self.lunch_end)
        self.ids["lunch_end"] = lunch_end

        punch_out = Button(text="Punch Out", disabled=True)
        punch_out.bind(on_press=self.punch_out)
        self.ids["punch_out"] = punch_out

        button_layout.add_widget(punch_in)
        button_layout.add_widget(lunch_start)
        button_layout.add_widget(lunch_end)
        button_layout.add_widget(punch_out)

        self.add_widget(button_layout)

    def punch_in(self, instance, *args):
        print("Punch In")
        instance.disabled = True
        self.ids.lunch_start.disabled = False  # can now start lunch
        self.ids.punch_out.disabled = False  # can now punch out
        self.times["Start"] = datetime.now()
        print(self.times["Start"])

    def lunch_start(self, instance, *args):
        print("Start Lunch")
        instance.disabled = True
        self.ids.punch_out.disabled = True  # can't punch out
        self.ids.lunch_end.disabled = False  # can now end lunch
        self.times["Lunch Start"] = datetime.now()
        print(self.times["Lunch Start"])
        print(f"Worked for {self.times['Lunch Start'] - self.times['Start']}")

    def lunch_end(self, instance, *args):
        print("End Lunch")
        instance.disabled = True
        self.ids.punch_out.disabled = False  # can now punch out
        self.times["Lunch End"] = datetime.now()
        print(self.times["Lunch End"])
        print(f"Lunch break for {self.times['Lunch End'] - self.times['Lunch Start']}")

    def punch_out(self, instance, *args):
        print("Punch Out")
        instance.disabled = True
        self.times["End"] = datetime.now()
        print(self.times["End"])
        if "Lunch Start" in self.times:
            total_seconds = round(
                (
                    self.times["End"]
                    - self.times["Start"]
                    - (self.times["Lunch End"] - self.times["Lunch Start"])
                ).total_seconds()
            )
        else:
            total_seconds = round(
                (self.times["End"] - self.times["Start"]).total_seconds()
            )
        print(f"Worked for {total_seconds} seconds")

        m, s = divmod(total_seconds, 60)
        h, m = divmod(m, 60)
        elapsed_str = f"{h:02d}:{m:02d}:{s:02d}" if h > 0 else f"{m:02d}:{s:02d}"

        self.ids.display.text = f"Worked for {elapsed_str}"

        with open("punchcard.csv", "a") as f:
            f.write(
                ",".join(
                    [
                        datetime.now().strftime("%Y-%m-%d"),
                        self.times["Start"].strftime("%H:%M:%S"),
                        self.times["Lunch Start"].strftime("%H:%M:%S")
                        if "Lunch Start" in self.times
                        else "",
                        self.times["Lunch End"].strftime("%H:%M:%S")
                        if "Lunch End" in self.times
                        else "",
                        self.times["End"].strftime("%H:%M:%S"),
                        str(elapsed_str),
                        "\n",
                    ]
                )
            )
