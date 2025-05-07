from pyqtier.widgets import PyQtierWidgetBase

from app import config
from app.views import Ui_AccelerationConfig


class AccelerationConfigWidget(PyQtierWidgetBase):
    def __init__(self):
        super().__init__(view_class=Ui_AccelerationConfig, config=config)