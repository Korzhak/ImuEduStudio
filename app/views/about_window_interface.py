# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Projects\Python\ImuEdu\app\views\templates\about_window_interface.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AboutView(object):
    def setupUi(self, AboutView):
        AboutView.setObjectName("AboutView")
        AboutView.resize(281, 246)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/img/information.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        AboutView.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(AboutView)
        self.gridLayout.setObjectName("gridLayout")
        self.lb_app_logo = QtWidgets.QLabel(AboutView)
        self.lb_app_logo.setMaximumSize(QtCore.QSize(150, 150))
        self.lb_app_logo.setText("")
        self.lb_app_logo.setPixmap(QtGui.QPixmap(":/icons/img/snake_logo.png"))
        self.lb_app_logo.setScaledContents(True)
        self.lb_app_logo.setObjectName("lb_app_logo")
        self.gridLayout.addWidget(self.lb_app_logo, 0, 0, 1, 1)
        self.lb_app_name = QtWidgets.QLabel(AboutView)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lb_app_name.setFont(font)
        self.lb_app_name.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_app_name.setObjectName("lb_app_name")
        self.gridLayout.addWidget(self.lb_app_name, 1, 0, 1, 1)
        self.lb_app_version = QtWidgets.QLabel(AboutView)
        self.lb_app_version.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_app_version.setObjectName("lb_app_version")
        self.gridLayout.addWidget(self.lb_app_version, 2, 0, 1, 1)
        self.lb_company_name = QtWidgets.QLabel(AboutView)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lb_company_name.setFont(font)
        self.lb_company_name.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_company_name.setObjectName("lb_company_name")
        self.gridLayout.addWidget(self.lb_company_name, 3, 0, 1, 1)

        self.retranslateUi(AboutView)
        QtCore.QMetaObject.connectSlotsByName(AboutView)

    def retranslateUi(self, AboutView):
        _translate = QtCore.QCoreApplication.translate
        AboutView.setWindowTitle(_translate("AboutView", "About"))
        self.lb_app_name.setText(_translate("AboutView", "App Name"))
        self.lb_app_version.setText(_translate("AboutView", "Version"))
        self.lb_company_name.setText(_translate("AboutView", "Company Name"))
from app.views import resources_rc
