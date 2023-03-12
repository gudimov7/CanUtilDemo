from textual.app import ComposeResult
from textual.reactive import reactive
from textual.widgets import Button, Static


class BoolDisplay(Static):

    def set_value(self, b: bool) -> None:
        self.update(f"{b}")


class SwitchBlock(Static):

    def __init__(self, name, callback):
        super().__init__()
        self.callback = None
        self.block_name = name
        self.callback = callback

    def set_value(self, value: bool):

        self.value = value

        if self.bool_display is not None:
            self.bool_display.set_value(self.value)

        return self

    def compose(self) -> ComposeResult:
        yield Static(self.block_name, id="lable")
        yield Button("send", id="send", variant="success")

    def on_button_pressed(self, event: Button.Pressed) -> None:

        button_id = event.button.id
        assert button_id is not None

        if button_id == "send":
            if self.callback:
                self.callback()


class ValueBlock(Static):

    def __init__(self, id, header):
        super().__init__(id=id, classes="value-block-" + header)
        self.header = header
        self.value_display = Static("---", id="value")

    def set_value(self, n: str):
        self.value_display.update(n)
        return self

    def reset(self):
        self.value_display.update("---")

    def compose(self) -> ComposeResult:
        yield Static(self.header, id="device-label")
        yield self.value_display


class MultiLineValueBlock(Static):
    def __init__(self, id, header):
        super().__init__(id=id, classes="value-block-" + header)
        self.header = header
        self.def_value = "---"
        self.value = self.def_value
        self.value_display = Static(self.def_value, id="multi-value")

    def set_value(self, n: str):
        if self.value == self.def_value:
            self.value = ""
        self.value += '\n' + n
        self.value_display.update(self.value)
        return self

    def reset(self):
        self.value = self.def_value
        self.value_display.update(self.def_value)

    def compose(self) -> ComposeResult:
        yield Static(self.header, id="device-label")
        yield self.value_display
