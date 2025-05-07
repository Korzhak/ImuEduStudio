import json

import numpy as np
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from pyqtgraph.dockarea.Dock import Dock
from pyqtgraph.dockarea.DockArea import DockArea
from pyqtier.widgets import PyQtierMainWindow

from app.widgets.acceleration_config_widget import AccelerationConfigWidget
from app.widgets.angular_rate_config_widget import AngularRateConfigWidget
from app.widgets.control_rotation_stand_widget import ControlRotationStandWidget
from app.widgets.tree_axis_plot_widget import (
    GyroscopeWidget,
    AccelerometerWidget,
    EulerAnglesWidget,
    RotatorAngleWidget,
    RotatorSpeedWidget
)

class MainWindow(PyQtierMainWindow):
    open_settings = pyqtSignal()
    open_about = pyqtSignal()

    def __init__(self, *args, **kwargs):
        self.control_rotation_stand_widget = None
        self.angular_rate_config_widget = None
        self.acceleration_config_widget = None
        self.dock_widgets = {}
        super().__init__(*args, **kwargs)

    def create_behavior(self):
        self.view.actionSettings.triggered.connect(self.open_settings.emit)
        self.view.actionAbout.triggered.connect(self.open_about.emit)
        # self.view.rb_degrees.clicked.connect(lambda: self.gyroscope_widget.clear())
        # self.view.rb_radians.clicked.connect(lambda: self.gyroscope_widget.clear())

        # self.view.rb_g.clicked.connect(lambda: self.accelerometer_widget.clear())
        # self.view.rb_m_sec_2.clicked.connect(lambda: self.accelerometer_widget.clear())
        # self.view.rb_send_angle.clicked.connect(self.allow_send_angle_callback)
        # self.view.rb_send_rotation.clicked.connect(self.allow_send_rotation_callback)

    def setup_view(self):
        self.angular_rate_config_widget = AngularRateConfigWidget()
        self.acceleration_config_widget = AccelerationConfigWidget()
        self.control_rotation_stand_widget = ControlRotationStandWidget()
        self.create_plots()

        # self.dock_widgets['gyro_config_dock_widget'] = self.view.gyro_config_dock_widget
        # self.dock_widgets['accel_config_dock_widget'] = self.view.accel_config_dock_widget
        # self.dock_widgets['rotator_config_dock_widget'] = self.view.rotator_config_dock_widget
        # self.dock_widgets['rotator_speed_dock_widget'] = self.view.rotator_speed_dock_widget
        # self.dock_widgets['rotation_angle_dock_widget'] = self.view.rotation_angle_dock_widget
        # self.create_menu()
        self.allow_send_rotation_callback()

    @pyqtSlot(int)
    def set_counter(self, data):
        print(data)

    def create_plots(self):
        self.dock_area = DockArea()
        self.setCentralWidget(self.dock_area)

        self.rotator_speed_widget = RotatorSpeedWidget()
        self.rotator_angle_widget = RotatorAngleWidget()
        self.angular_rate_plot_widget = GyroscopeWidget()
        self.accelerometer_widget = AccelerometerWidget()
        self.euler_angles_widget = EulerAnglesWidget()

        self.add_dock_widget(
            "Прискорення",
            "accel_dock",
            self.accelerometer_widget
        )
        self.add_dock_widget(
            "Налаштування прискорення",
            "acceleration_config_dock",
            self.acceleration_config_widget
        )
        self.add_dock_widget(
            "Кутова швидкість",
            "angular_rate_dock",
            self.angular_rate_plot_widget
        )
        self.add_dock_widget(
            "Налаштування кутової швидкості",
            "angular_rate_config_dock",
            self.angular_rate_config_widget
        )
        self.add_dock_widget(
            "Кути Ейлера",
            "euler_dock",
            self.euler_angles_widget
        )
        self.add_dock_widget(
            "Кут обертового стенду",
            "rotator_angle_dock",
            self.rotator_angle_widget,
            closable=True
        )
        self.add_dock_widget(
            "Кутова швидкість обертового стенду",
            "rotator_speed_dock",
            self.rotator_speed_widget,
            closable=True
        )

        self.add_dock_widget(
            "Керування обертовим стендом",
            "control_rotation_stand_widget",
            self.control_rotation_stand_widget,
            closable=True
        )

        # self.dock_area.addDock(self.angular_rate_config_dock)
        # self.dock_area.addDock(self.acceleration_config_dock)
        # self.dock_area.addDock(self.control_rotation_stand_dock)

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
        self.angular_rate_plot_widget.update_data(processed_gyro_data)

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
        # self.view.sb_rotator_angle.setDisabled(True)
        # self.view.sb_rotator_rotation.setDisabled(False)
        ...

    def add_dock_widget(self, name, short_name, widget, size=(10, 10), closable=False ):
        self.dock_widgets[short_name] = Dock(name, closable=closable, size=size, autoOrientation=False)
        self.dock_widgets[short_name].addWidget(widget)
        self.dock_area.addDock(self.dock_widgets[short_name])

    def _save_additional_state(self):
        """Save dock state to Windows registry"""
        # Get the dock area state
        state = self.dock_area.saveState()
        # Convert to JSON string (registry can store strings)
        state_json = json.dumps(state)

        # Write to registry
        self.settings.setValue("dockAreaState", state_json)

    def _restore_additional_state(self):
        """Load dock state from Windows registry"""
        # Read from registry
        state_json = self.settings.value("dockAreaState")

        # If we have a saved state, restore it
        if state_json:
            try:
                # Convert JSON string back to dict
                state = json.loads(state_json)

                # Restore dock state
                self.dock_area.restoreState(state)
            except Exception as e:
                print(f"Error restoring dock state: {e}")