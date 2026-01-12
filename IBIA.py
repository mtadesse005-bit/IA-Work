from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.screen import MDScreen

class SimpleApp(MDApp):
    def build(self):
        screen = MDScreen()
        
        # A simple button in the middle
        btn = MDRectangleFlatButton(
            text="Click Me!",
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            on_release=self.change_text
        )
        
        screen.add_widget(btn)
        return screen

    def change_text(self, button):
        button.text = "It Worked!"
        button.md_bg_color = (0, 1, 0, 1) # Changes to Green

SimpleApp().run()



