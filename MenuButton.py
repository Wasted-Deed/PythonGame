import arcade
import arcade.gui
from arcade.gui import UIManager

class PlayButton(arcade.gui.UIFlatButton):
    def __init__(self):
        super().__init__(
            text = "Играть", 
            center_x = 0,
            center_y = 0,
            width = 250,
            height = 30,
            id = 0
        )
        self.click = False

    def on_click(self):
        self.click = True

class ExitButton(arcade.gui.UIFlatButton):
    def __init__(self):
        super().__init__(
            text = "Настройки",
            center_x = 0,
            center_y = 0,
            width = 250,
            height = 30,
            id = 1
        )
        self.click = False

    def on_click(self):
        self.click = True

class SettingButton(arcade.gui.UIFlatButton):
    def __init__(self):
        super().__init__(
            text = "Выход",
            center_x = 0,
            center_y = 0,
            width = 250,
            height = 30,
            id = 2
        )
        self.click = False

    def on_click(self):
        self.click = True