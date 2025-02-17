import numpy as np
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
        self.view.rb_degrees.clicked.connect(lambda: self.gyroscope_widget.clear())
        self.view.rb_radians.clicked.connect(lambda: self.gyroscope_widget.clear())

        self.view.rb_g.clicked.connect(lambda: self.accelerometer_widget.clear())
        self.view.rb_m_sec_2.clicked.connect(lambda: self.accelerometer_widget.clear())
        self.view.rb_send_angle.clicked.connect(self.allow_send_angle_callback)
        self.view.rb_send_rotation.clicked.connect(self.allow_send_rotation_callback)

    def setup_view(self):
        self.create_plots()
        self.dock_widgets['gyro_config_dock_widget'] = self.view.gyro_config_dock_widget
        self.dock_widgets['accel_config_dock_widget'] = self.view.accel_config_dock_widget
        self.dock_widgets['rotator_config_dock_widget'] = self.view.rotator_config_dock_widget
        self.dock_widgets['rotator_speed_dock_widget'] = self.view.rotator_speed_dock_widget
        self.dock_widgets['rotation_angle_dock_widget'] = self.view.rotation_angle_dock_widget
        self.create_menu()
        self.allow_send_rotation_callback()

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

    def preprocessing_gyro_data(self, data: dict):
        processed_data = data.copy()

        if self.view.rb_degrees.isChecked():
            processed_data['x'] = np.rad2deg(processed_data['x'])
            processed_data['y'] = np.rad2deg(processed_data['y'])
            processed_data['z'] = np.rad2deg(processed_data['z'])

        if self.view.cb_accept_gyro_x_bias.isChecked():
            processed_data['x'] -= self.view.sb_bias_x_gyro.value()

        if self.view.cb_accept_gyro_y_bias.isChecked():
            processed_data['y'] -= self.view.sb_bias_y_gyro.value()

        if self.view.cb_accept_gyro_z_bias.isChecked():
            processed_data['z'] -= self.view.sb_bias_z_gyro.value()

        return processed_data

    def preprocessing_accel_data(self, data: dict):
        processed_data = data.copy()

        if self.view.rb_g.isChecked():
            processed_data['x'] /= 9.81
            processed_data['y'] /= 9.81
            processed_data['z'] /= 9.81

        return processed_data

    def obtain_data(self, data: dict):
        # Gyroscope data
        processed_gyro_data = self.preprocessing_gyro_data(data['gyro'])
        self.gyroscope_widget.update_data(processed_gyro_data)

        self.view.lb_gyro_x_value.setText(str(np.round(processed_gyro_data['x'], 2)))
        self.view.lb_gyro_y_value.setText(str(np.round(processed_gyro_data['y'], 2)))
        self.view.lb_gyro_z_value.setText(str(np.round(processed_gyro_data['z'], 2)))

        # Accelerometer data
        processed_accel_data = self.preprocessing_accel_data(data['accel'])
        self.accelerometer_widget.update_data(processed_accel_data)

        self.view.lb_accel_x_value.setText(str(np.round(processed_accel_data['x'], 3)))
        self.view.lb_accel_y_value.setText(str(np.round(processed_accel_data['y'], 3)))
        self.view.lb_accel_z_value.setText(str(np.round(processed_accel_data['z'], 3)))

    def allow_send_angle_callback(self):
        self.view.sb_rotator_angle.setDisabled(False)
        self.view.sb_rotator_rotation.setDisabled(True)

    def allow_send_rotation_callback(self):
        self.view.sb_rotator_angle.setDisabled(True)
        self.view.sb_rotator_rotation.setDisabled(False)
