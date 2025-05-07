from pyqtier.widgets import PyQtierWidgetBase

from app import config
from app.views import Ui_ControlRotationStand


class ControlRotationStandWidget(PyQtierWidgetBase):
    def __init__(self):
        super().__init__(view_class=Ui_ControlRotationStand, config=config)