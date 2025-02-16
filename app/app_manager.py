from pyqtier import PyQtierApplicationManager
from pyqtier.plugins import UsbPluginManager

from app import config
from app.utils.usb_processor import DataProcessor
from app.views import Ui_MainWindow
from app.views import Ui_SimpleView, Ui_AboutView
from app.widgets import MainWindow, SettingsWindow, AboutWindow


class ApplicationManager(PyQtierApplicationManager):
    def __init__(self):
        self.usb_manager = None
        self.data_processor = None
        self.about_window = None
        self.settings_window = None
        super().__init__()

    def setup_manager(self):
        self.main_window = MainWindow(view_class=Ui_MainWindow, config=config)
        self.settings_window = SettingsWindow(view_class=Ui_SimpleView, config=config)
        self.about_window = AboutWindow(view_class=Ui_AboutView, config=config)
        self.setup_usb()

    def create_behaviour(self):
        self.main_window.open_settings.connect(self.settings_window.show)
        self.main_window.open_about.connect(self.about_window.show)
        self.settings_window.button_signal.connect(self.main_window.set_counter)

    def setup_usb(self):
        self.data_processor = DataProcessor()

        self.usb_manager = UsbPluginManager(with_baudrate=True, default_baudrate=115200)
        self.usb_manager.setup_view(self.main_window.view.devices_widget, self.main_window.view.statusbar)
        self.usb_manager.set_data_processor(self.data_processor)

        self.usb_manager.set_obtain_data_callback(self.obtain_data_callback)
        self.usb_manager.set_error_callback(self.obtain_error_callback)
        self.usb_manager.set_connection_lost_callback(self.connection_lost_callback)
        self.usb_manager.set_connect_callback(self.connect_callback)
        self.usb_manager.set_disconnect_callback(self.disconnect_callback)

    # @pyqtSlot(dict)
    def obtain_data_callback(self, data):
        self.main_window.obtain_data(data)

    # @pyqtSlot(str)
    def obtain_error_callback(self, error):
        print(f"Error: {error}")

    # @pyqtSlot()
    def connection_lost_callback(self):
        print("connection lost")

    # @pyqtSlot()
    def connect_callback(self):
        print("device connected")

    # @pyqtSlot()
    def disconnect_callback(self):
        print("device disconnected")
