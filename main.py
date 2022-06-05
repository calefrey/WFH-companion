from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.config import Config
from os.path import exists as file_exists
from PunchClock import PunchClock

Config.set("graphics", "width", "400")
Config.set("graphics", "height", "100")

if not file_exists("punchcard.csv"):
    with open("punchcard.csv", "w") as f:
        f.write("Date,Start,Lunch Start,Lunch End,End,Total Time\n")


class MainApp(App):
    def build(self):
        self.title = "Punch Clock"
        layout = BoxLayout(orientation="vertical")
        layout.add_widget(PunchClock())
        return layout


if __name__ == "__main__":
    MainApp().run()
