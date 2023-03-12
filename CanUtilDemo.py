import can

from datetime import datetime
from can_receiver import CanReceiver
from can_sender import CanSender
from common_ui import SwitchBlock, ValueBlock, MultiLineValueBlock
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Header, Footer, Checkbox


class CanUtilApp(App):
    TITLE: str = "Can Util App"
    CSS_PATH = "app_ui.css"
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("r", "reset", "Reset")
    ]

    def __init__(self):
        super().__init__()
        # self.channel = 'vcan0'
        self.channel = 'can0'
        self.can_sender = CanSender(name="sender", chanel=self.channel)
        self.can_monitor = CanReceiver(name="receiver", chanel=self.channel, callback=self.monitor_can)

        self.msg_header = "N/A"
        self.msg_content = "N/A"

        self.container = None
        self.display_widget: ValueBlock = None
        self.monitor_widget: ValueBlock = None

    def action_quit(self) -> None:
        self.can_sender.close()
        self.can_monitor.close()
        self.exit()

    def action_reset(self) -> None:
        if self.display_widget is not None:
            self.display_widget.reset()

        if self.monitor_widget is not None:
            self.monitor_widget.reset()

    def compose(self) -> ComposeResult:
        self.container = Container(id="container")

        widget_std = SwitchBlock(name="Can std",
                                 callback=self.send_std_can)

        widget_ext = SwitchBlock(name="Can ext",
                                 callback=self.send_ext_can)

        self.display_widget = ValueBlock("send-dsp", self.channel)
        self.monitor_widget = MultiLineValueBlock("recv-dsp", "MONITOR")

        self.container.mount(widget_std)
        self.container.mount(widget_ext)
        self.container.mount(self.display_widget)
        self.container.mount(self.monitor_widget)

        yield Header()
        yield self.container
        yield Footer()

    def send_std_can(self):
        data = [11, 22, 33, 44, 55, 66, 77, 88]
        ret = self.can_sender.send_msg(msg_id=123, msg=bytearray(data))
        self.display_widget.set_value(ret)
        print("send_std_can")

    def send_ext_can(self):
        data = [0xA, 0xB, 0xC, 0xD, 0xE, 0xF, 0xEE, 0xEE, 0xAA, 0xAB, 0xAC, 0xAD, 0xAE, 0xAF, 0xEE, 0xEE]
        ret = self.can_sender.send_msg(msg_id=123, msg=bytearray(data), is_ext=True)
        self.display_widget.set_value(ret)
        print("send_ext_can")

    def monitor_can(self, msg: can.Message):
        time = datetime.fromtimestamp(msg.timestamp)
        msg_id = msg.arbitration_id
        msg_len = msg.dlc
        data = ''.join('{:02X} '.format(x) for x in msg.data)

        self.monitor_widget.set_value(
            f"{time}: [{msg_id}][{msg_len}][{data}] FD[{msg.is_fd}]")


if __name__ == "__main__":
    app = CanUtilApp()
    app.run()
