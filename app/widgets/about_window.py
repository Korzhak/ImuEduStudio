from pyqtier.widgets import PyQtierWidgetBase


class AboutWindow(PyQtierWidgetBase):
    def setup_view(self):
        self.setWindowTitle("About App")
        self.view.lb_app_name.setText(self.configs.APP_NAME)
        self.view.lb_app_version.setText(self.configs.APP_VERSION)
        self.view.lb_company_name.setText(self.configs.COMPANY_NAME)
