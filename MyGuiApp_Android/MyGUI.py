#!/usr/bin/python3
# -*- coding: utf8 -*-

import sys;
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget, QMessageBox;
from PyQt5.QtWidgets import QApplication;  #used for GUI applcation
from PyQt5.QtCore import QCoreApplication; #used for console application
from PyQt5.QtCore import pyqtSignal, pyqtSlot;
from intent_android import MsgApp;

import Login;

class MyApp(MsgApp):
    def __init__(self):
        MsgApp.__init__(self);
        self.__app = None,
        self.__mainWindow = None;
        self.__ui = None;
        self.__text = "";
        self.__number = 100;
    
    def __del__(self):
        MsgApp.__del__(self);
        pass;
    
    def prepare(self, argv):
        self.__app = QApplication(argv);
        self.__mainWindow = QMainWindow();
        self.__ui = Login.Ui_MyDialog();
        self.__ui.setupUi(self.__mainWindow);
        
        #self.__ui.btnReset.clicked.connect(QApplication.instance().quit);
        self.__ui.btnReset.clicked.connect(QApplication.instance().exit);
        #self.__ui.btnReset.clicked.connect(QCoreApplication.instance().quit);
        #self.__ui.btnReset.clicked.connect(QCoreApplication.instance().exit);
        self.__ui.btnLogin.clicked.connect(self.doLogin);
        self.__ui.btnReset.clicked.connect(self.doReset);
        self.__ui.btnSendMsg.clicked.connect(self.send_message);
        return True;
    
    def doLogin(self):
        ret = QMessageBox.question(self.__mainWindow, "Prompt", "Are you sure to login?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No);
        
        if(ret == QMessageBox.Yes):
            msg = "UserName: %s\nPassword: %s" % (self.__ui.edtUserName.text(), self.__ui.edtPassword.text());
            QMessageBox.information(self.__mainWindow, "信息", msg, QMessageBox.Yes | QMessageBox.No, QMessageBox.No);
            self.__ui.edtMsg.setText("LoginXXX ......");
        else:
            self.__ui.edtMsg.setText("CancelXX ......");
        return True;
    
    def doReset(self):
        print("111111");
        self.__ui.edtUserName.setText();
        self.__ui.edtPassword.setText();
        print("222222");
    
    #该函数留给子类实现:
    def filter_message(self, msg):
        print("WARN: the member MyApp.filter_message() have not been implemented");
        return False;
    
    #该函数留给子类实现:
    def handle_message(self, msg):
        _what = msg.get_what();
        tmp = "处理消息 " + str(_what);
        #text = self.__ui.edtMsg.toPlainText();
        #text = text + "\n" + tmp;
        #self.__ui.edtMsg.setPlainText(tmp);
        print(tmp);
        return True;
    
    #该函数留给子类实现:
    def message_callback(self, msg, result):
        _what = msg.get_what();
        print("消息 " + str(_what) + " have done, result = " + str(result));
        return True;
    
    def send_message(self):
        self.__number = self.__number + 1;
        self.post_message(what = self.__number, need_callback = True, target = self);
    
    def doRun(self):
        self.__mainWindow.show();
        sys.exit(self.__app.exec_());

if __name__ == '__main__':
    app1 = MyApp();
    app1.prepare(sys.argv);
    #app1.runAsAlone();
    app1.doRun();
