import random
from collections import deque

import pyqtgraph as pg
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QCheckBox)
from PyQt5.QtCore import Qt


class ThreeAxisPlotWidget(QWidget):
    """Базовий клас для відображення графіків по трьох осях"""

    def __init__(self, title="Three Axis Plot", y_label="Value", units="", parent=None):
        super().__init__(parent)
        self.title = title
        self.y_label = y_label
        self.units = units
        self.initUI()
        self.x_vis = True
        self.y_vis = True
        self.z_vis = True

        self.t_previous = 0

    def initUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Налаштовуємо графік
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground(pg.mkColor(67, 67, 67))
        self.plot_widget.setLabel('left', self.y_label, units=self.units)
        self.plot_widget.setLabel('bottom', 'Час', units='с')
        self.plot_widget.setTitle(self.title)
        self.plot_widget.showGrid(x=True, y=True)

        # Створюємо буфери для даних
        self.max_points = 300
        self.times = deque(maxlen=self.max_points)
        self.x_data = deque(maxlen=self.max_points)
        self.y_data = deque(maxlen=self.max_points)
        self.z_data = deque(maxlen=self.max_points)

        # Створюємо криві для кожної осі
        self.x_curve = self.plot_widget.plot(pen=pg.mkPen('r', width=1.5), name='X')
        self.y_curve = self.plot_widget.plot(pen=pg.mkPen('g', width=1.5), name='Y')
        self.z_curve = self.plot_widget.plot(pen=pg.mkPen('b', width=1.5), name='Z')

        # Створюємо і налаштовуємо легенду
        self.legend = self.plot_widget.addLegend()

        # Створюємо окремі items для легенди
        self.x_legend_item = self.legend.addItem(self.x_curve, 'X')
        self.y_legend_item = self.legend.addItem(self.y_curve, 'Y')
        self.z_legend_item = self.legend.addItem(self.z_curve, 'Z')

        main_layout.addWidget(self.plot_widget)

        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.update_plots)
        self.timer.start(30)

        self.time = 0

    def legend_clicked(self, event, item):
        """Обробник кліку по елементу легенди"""
        if event.button() == Qt.LeftButton:
            # Визначаємо, який елемент легенди був натиснутий
            if item == self.x_legend_item:
                self.x_vis = not self.x_vis
                self.x_curve.setVisible(self.x_vis)
            elif item == self.y_legend_item:
                self.y_vis = not self.y_vis
                self.y_curve.setVisible(self.y_vis)
            elif item == self.z_legend_item:
                self.z_vis = not self.z_vis
                self.z_curve.setVisible(self.z_vis)

    def update_visibility(self, x_vis, y_vis, z_vis):
        self.x_vis = x_vis
        self.y_vis = y_vis
        self.z_vis = z_vis
        self.x_curve.setVisible(x_vis)
        self.y_curve.setVisible(y_vis)
        self.z_curve.setVisible(z_vis)

    def update_data(self, data):
        """Метод для оновлення даних, має бути перевизначений у нащадках"""
        self.time += 0.05
        self.times.append(self.time)

        # За замовчуванням генеруємо випадкові дані
        self.x_data.append(data['x'])
        self.y_data.append(data['y'])
        self.z_data.append(data['z'])

    def update_plots(self):
        if self.x_vis:
            self.x_curve.setData(list(self.times), list(self.x_data))
        if self.y_vis:
            self.y_curve.setData(list(self.times), list(self.y_data))
        if self.z_vis:
            self.z_curve.setData(list(self.times), list(self.z_data))


class TwoAxisPlotWidget(QWidget):
    """Базовий клас для відображення графіків по двох осях"""

    def __init__(self, title="Two Axis Plot", y_label="Value", units="", parent=None):
        super().__init__(parent)
        self.title = title
        self.y_label = y_label
        self.units = units
        self.initUI()
        self.x_vis = True
        self.y_vis = True

    def initUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Налаштовуємо графік
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground(pg.mkColor(67, 67, 67))
        self.plot_widget.setLabel('left', self.y_label, units=self.units)
        self.plot_widget.setLabel('bottom', 'Час', units='с')
        self.plot_widget.setTitle(self.title)
        self.plot_widget.showGrid(x=True, y=True)

        # Створюємо буфери для даних
        self.max_points = 100
        self.times = deque(maxlen=self.max_points)
        self.x_data = deque(maxlen=self.max_points)
        self.y_data = deque(maxlen=self.max_points)

        # Створюємо криві для кожної осі
        self.x_curve = self.plot_widget.plot(pen=pg.mkPen('r', width=1.5), name='X')
        self.y_curve = self.plot_widget.plot(pen=pg.mkPen('g', width=1.5), name='Y')

        # Створюємо і налаштовуємо легенду
        self.legend = self.plot_widget.addLegend()

        # Створюємо окремі items для легенди
        self.x_legend_item = self.legend.addItem(self.x_curve, 'X')
        self.y_legend_item = self.legend.addItem(self.y_curve, 'Y')

        main_layout.addWidget(self.plot_widget)

        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(50)

        self.time = 0

    def legend_clicked(self, event, item):
        """Обробник кліку по елементу легенди"""
        if event.button() == Qt.LeftButton:
            if item == self.x_legend_item:
                self.x_vis = not self.x_vis
                self.x_curve.setVisible(self.x_vis)
            elif item == self.y_legend_item:
                self.y_vis = not self.y_vis
                self.y_curve.setVisible(self.y_vis)

    def update_visibility(self, x_vis, y_vis):
        self.x_vis = x_vis
        self.y_vis = y_vis
        self.x_curve.setVisible(x_vis)
        self.y_curve.setVisible(y_vis)

    def update_data(self):
        """Метод для оновлення даних, має бути перевизначений у нащадках"""
        self.time += 0.05
        self.times.append(self.time)

        # За замовчуванням генеруємо випадкові дані
        self.x_data.append(random.uniform(-10, 10))
        self.y_data.append(random.uniform(-10, 10))

        if self.x_vis:
            self.x_curve.setData(list(self.times), list(self.x_data))
        if self.y_vis:
            self.y_curve.setData(list(self.times), list(self.y_data))


class OneAxisPlotWidget(QWidget):
    """Базовий клас для відображення графіка по одній осі"""

    def __init__(self, title="One Axis Plot", y_label="Value", units="", parent=None):
        super().__init__(parent)
        self.title = title
        self.y_label = y_label
        self.units = units
        self.initUI()
        self.x_vis = True

    def initUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Налаштовуємо графік
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground(pg.mkColor(67, 67, 67))
        self.plot_widget.setLabel('left', self.y_label, units=self.units)
        self.plot_widget.setLabel('bottom', 'Час', units='с')
        self.plot_widget.setTitle(self.title)
        self.plot_widget.showGrid(x=True, y=True)

        # Створюємо буфери для даних
        self.max_points = 100
        self.times = deque(maxlen=self.max_points)
        self.x_data = deque(maxlen=self.max_points)

        # Створюємо криву
        self.x_curve = self.plot_widget.plot(pen=pg.mkPen('r', width=1.5), name='X')

        # Створюємо і налаштовуємо легенду
        self.legend = self.plot_widget.addLegend()

        # Створюємо item для легенди
        self.x_legend_item = self.legend.addItem(self.x_curve, 'X')

        main_layout.addWidget(self.plot_widget)

        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(50)

        self.time = 0

    def legend_clicked(self, event, item):
        """Обробник кліку по елементу легенди"""
        if event.button() == Qt.LeftButton:
            self.x_vis = not self.x_vis
            self.x_curve.setVisible(self.x_vis)

    def update_visibility(self, x_vis):
        self.x_vis = x_vis
        self.x_curve.setVisible(x_vis)

    def update_data(self):
        """Метод для оновлення даних, має бути перевизначений у нащадках"""
        self.time += 0.05
        self.times.append(self.time)

        # За замовчуванням генеруємо випадкові дані
        self.x_data.append(random.uniform(-10, 10))

        if self.x_vis:
            self.x_curve.setData(list(self.times), list(self.x_data))


class OneAxisExample(OneAxisPlotWidget):
    def __init__(self, parent=None):
        super().__init__(
            title="Приклад однієї осі",
            y_label="Значення",
            units="од",
            parent=parent
        )


class GyroscopeWidget(ThreeAxisPlotWidget):
    """Віджет для відображення даних гіроскопа"""

    def __init__(self, parent=None):
        super().__init__(
            title="Дані кутової швидкості",
            y_label="Кутова швидкість",
            units="рад/с",
            parent=parent
        )


class AccelerometerWidget(ThreeAxisPlotWidget):
    """Віджет для відображення даних акселерометра"""

    def __init__(self, parent=None):
        super().__init__(
            title="Дані прискорення",
            y_label="Прискорення",
            units="g",
            parent=parent
        )


class MagnetometerWidget(ThreeAxisPlotWidget):
    """Віджет для відображення даних магнітометра"""

    def __init__(self, parent=None):
        super().__init__(
            title="Magnetometer Data",
            y_label="Magnetic Field",
            units="µT",
            parent=parent
        )


class EulerAnglesWidget(ThreeAxisPlotWidget):
    """Віджет для відображення даних кутів Ейлера"""

    def __init__(self, parent=None):
        super().__init__(
            title="Значення кутів Ейлера",
            y_label="Кути Ейлера",
            units="рад",
            parent=parent
        )


# Приклад використання:
class RotatorSpeedWidget(OneAxisPlotWidget):
    def __init__(self, parent=None):
        super().__init__(
            title="Швидкість обертального стенду",
            y_label="Значення",
            units="крок/с",
            parent=parent
        )


class RotatorAngleWidget(OneAxisPlotWidget):
    def __init__(self, parent=None):
        super().__init__(
            title="Кут обертального стенду",
            y_label="Значення",
            units="рад",
            parent=parent
        )
