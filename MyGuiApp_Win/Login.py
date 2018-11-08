# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5.QtWidgets import QMainWindow;
from PyQt5 import QtCore, QtGui, QtWidgets;

class Ui_MyDialog(QMainWindow):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(690, 420)
        self.lblUserName = QtWidgets.QLabel(Dialog)
        self.lblUserName.setGeometry(QtCore.QRect(40, 40, 41, 16))
        self.lblUserName.setObjectName("lblUserName")
        self.edtUserName = QtWidgets.QLineEdit(Dialog)
        self.edtUserName.setGeometry(QtCore.QRect(80, 40, 113, 21))
        self.edtUserName.setObjectName("edtUserName")
        self.lblPassword = QtWidgets.QLabel(Dialog)
        self.lblPassword.setGeometry(QtCore.QRect(40, 70, 41, 16))
        self.lblPassword.setObjectName("lblPassword")
        self.edtPassword = QtWidgets.QLineEdit(Dialog)
        self.edtPassword.setGeometry(QtCore.QRect(80, 70, 113, 21))
        self.edtPassword.setObjectName("edtPassword")
        self.btnLogin = QtWidgets.QPushButton(Dialog)
        self.btnLogin.setGeometry(QtCore.QRect(40, 100, 61, 28))
        self.btnLogin.setObjectName("btnLogin")
        self.btnReset = QtWidgets.QPushButton(Dialog)
        self.btnReset.setGeometry(QtCore.QRect(130, 100, 61, 28))
        self.btnReset.setObjectName("btnReset")
        self.btnSendMsg = QtWidgets.QPushButton(Dialog)
        self.btnSendMsg.setGeometry(QtCore.QRect(40, 240, 93, 28))
        self.btnSendMsg.setObjectName("btnSendMsg")
        self.edtMsg = QtWidgets.QTextEdit(Dialog)
        self.edtMsg.setGeometry(QtCore.QRect(40, 140, 191, 87))
        self.edtMsg.setObjectName("edtMsg")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "登录 "))
        self.lblUserName.setText(_translate("Dialog", "账号:"))
        self.lblPassword.setText(_translate("Dialog", "密码:"))
        self.btnLogin.setText(_translate("Dialog", "登录"))
        self.btnReset.setText(_translate("Dialog", "取消"))
        self.btnSendMsg.setText(_translate("Dialog", "发送消息"))

