from pyqtier.widgets import PyQtierMainWindow
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from app.widgets.tree_axis_plot_widget import (
    GyroscopeWidget,
    AccelerometerWidget,
    MagnetometerWidget,
    EulerAnglesWidget,
    RotatorAngleWidget,
    RotatorSpeedWidget
)


class MainWindow(PyQtierMainWindow):
    open_settings = pyqtSignal()
    open_about = pyqtSignal()

    def __init__(self, *args, **kwargs):
        self.dock_widgets = {}
        super().__init__(*args, **kwargs)

    def create_behavior(self):
        self.view.actionSettings.triggered.connect(self.open_settings.emit)
        self.view.actionAbout.triggered.connect(self.open_about.emit)

    def setup_view(self):
        self.create_plots()
        self.dock_widgets['gyro_config_dock_widget'] = self.view.gyro_config_dock_widget
        self.dock_widgets['accel_config_dock_widget'] = self.view.accel_config_dock_widget
        self.dock_widgets['rotator_speed_dock_widget'] = self.view.rotator_speed_dock_widget
        self.dock_widgets['rotation_angle_dock_widget'] = self.view.rotation_angle_dock_widget
        self.create_menu()

    @pyqtSlot(int)
    def set_counter(self, data):
        print(data)

    def create_plots(self):
        self.rotator_angle_widget = RotatorAngleWidget()
        self.rotator_speed_widget = RotatorSpeedWidget()

        self.gyroscope_widget = GyroscopeWidget()
        self.accelerometer_widget = AccelerometerWidget()
        self.euler_angles_widget = EulerAnglesWidget()

        self.rotator_angle_layout = QHBoxLayout()
        self.rotator_angle_layout.setContentsMargins(0, 0, 0, 0)
        self.view.rotation_angle_widget.setLayout(self.rotator_angle_layout)
        self.rotator_angle_layout.addWidget(self.rotator_angle_widget)

        self.rotator_speed_layout = QHBoxLayout()
        self.rotator_speed_layout.setContentsMargins(0, 0, 0, 0)
        self.view.rotation_speed_widget.setLayout(self.rotator_speed_layout)
        self.rotator_speed_layout.addWidget(self.rotator_speed_widget)

        self.accel_plot_layout = QHBoxLayout()
        self.accel_plot_layout.setContentsMargins(0, 0, 0, 0)
        self.view.accel_plot_widget.setLayout(self.accel_plot_layout)
        self.accel_plot_layout.addWidget(self.accelerometer_widget)

        self.gyro_plot_layout = QHBoxLayout()
        self.gyro_plot_layout.setContentsMargins(0, 0, 0, 0)
        self.view.gyro_plot_widget.setLayout(self.gyro_plot_layout)
        self.gyro_plot_layout.addWidget(self.gyroscope_widget)

        self.euler_angles_plot_layout = QHBoxLayout()
        self.euler_angles_plot_layout.setContentsMargins(0, 0, 0, 0)
        self.view.euler_plot_widget.setLayout(self.euler_angles_plot_layout)
        self.euler_angles_plot_layout.addWidget(self.euler_angles_widget)

    def create_menu(self):
        # Створюємо меню "Вигляд"
        self.view_menu = self.view.menubar.addMenu("Вигляд")

        # Додаємо дії для кожного dock widget
        for name, dock in self.dock_widgets.items():
            action = dock.toggleViewAction()
            action.setCheckable(True)
            action.setChecked(True)
            self.view_menu.addAction(action)

    def obtain_data(self, data: dict):
        self.gyroscope_widget.update_data(data["gyro"])
        self.accelerometer_widget.update_data(data['accel'])
