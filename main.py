
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from pathlib import Path

Window.clearcolor = get_color_from_hex("#080D19")

KV = """
ScreenManager:
    Home:
    Tools:
    Notes:

<Home>:
    name: "home"
    BoxLayout:
        orientation: "vertical"
        padding: 22
        spacing: 15

        Label:
            text: "[b]NOVA X[/b]"
            markup: True
            font_size: "36sp"
            color: 0.2, 0.75, 1, 1
            size_hint_y: None
            height: "85dp"

        Label:
            text: "YOUR PERSONAL SMART ASSISTANT"
            font_size: "12sp"
            color: 0.7, 0.8, 0.95, 1
            size_hint_y: None
            height: "35dp"

        Button:
            text: "AI ASSISTANT"
            on_release: app.ai_demo()

        Button:
            text: "SMART TOOLS"
            on_release: app.root.current = "tools"

        Button:
            text: "MY NOTES"
            on_release: app.root.current = "notes"

        Widget:

        Label:
            text: "NOVA X | VERSION 1.0"
            size_hint_y: None
            height: "35dp"

<Tools>:
    name: "tools"
    BoxLayout:
        orientation: "vertical"
        padding: 20
        spacing: 12

        Label:
            text: "[b]SMART CALCULATOR[/b]"
            markup: True
            font_size: "25sp"
            size_hint_y: None
            height: "55dp"

        TextInput:
            id: expression
            hint_text: "Example: 25 * 4 + 10"
            multiline: False
            size_hint_y: None
            height: "55dp"

        Button:
            text: "CALCULATE"
            size_hint_y: None
            height: "55dp"
            on_release: app.calculate(expression.text)

        Label:
            id: result
            text: "Your result appears here"

        Button:
            text: "BACK"
            size_hint_y: None
            height: "50dp"
            on_release: app.root.current = "home"

<Notes>:
    name: "notes"
    BoxLayout:
        orientation: "vertical"
        padding: 18
        spacing: 12

        Label:
            text: "[b]NOVA NOTES[/b]"
            markup: True
            font_size: "25sp"
            size_hint_y: None
            height: "55dp"

        TextInput:
            id: note
            hint_text: "Write your notes..."
            multiline: True

        Button:
            text: "SAVE NOTES"
            size_hint_y: None
            height: "55dp"
            on_release: app.save_note(note.text)

        Label:
            id: status
            text: ""

        Button:
            text: "BACK"
            size_hint_y: None
            height: "50dp"
            on_release: app.root.current = "home"
"""

class Home(Screen):
    pass

class Tools(Screen):
    pass

class Notes(Screen):
    pass


class NovaX(App):

    def build(self):
        self.title = "NOVA X"
        return Builder.load_string(KV)

    def ai_demo(self):
        Popup(
            title="NOVA AI",
            content=Label(
                text="Welcome to NOVA X!\\n"
                     "AI connection will be added later."
            ),
            size_hint=(0.85, 0.35)
        ).open()

    def calculate(self, expression):
        import ast
        import operator

        ops = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow
        }

        def evaluate(node):
            if isinstance(node, ast.Constant):
                if type(node.value) in (int, float):
                    return node.value

            if isinstance(node, ast.BinOp) and type(node.op) in ops:
                a = evaluate(node.left)
                b = evaluate(node.right)

                if isinstance(node.op, ast.Pow) and abs(b) > 10:
                    raise ValueError()

                return ops[type(node.op)](a, b)

            raise ValueError()

        try:
            result = evaluate(ast.parse(expression, mode="eval").body)
            self.root.get_screen("tools").ids.result.text = str(result)
        except Exception:
            self.root.get_screen("tools").ids.result.text = "Invalid expression"

    def save_note(self, content):
        try:
            path = Path(self.user_data_dir) / "nova_notes.txt"
            path.write_text(content, encoding="utf-8")
            self.root.get_screen("notes").ids.status.text = "Saved successfully!"
        except OSError:
            self.root.get_screen("notes").ids.status.text = "Save failed"

NovaX().run()
