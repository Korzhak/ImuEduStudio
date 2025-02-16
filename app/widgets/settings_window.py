from pyqtier.widgets import PyQtierWidgetBase
from PyQt5.QtCore import pyqtSignal


class SettingsWindow(PyQtierWidgetBase):
    button_signal = pyqtSignal(int)
    counter: int = 0

    def create_behavior(self):
        self.view.bt_1.clicked.connect(self.bt_callback)

    def bt_callback(self):
        self.counter += 1
        self.button_signal.emit(self.counter)
