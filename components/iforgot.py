# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ui\iforgot_test.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import smtplib, ssl
import hashlib
from database import Database
from uuid import uuid4
from validate import validateEmail, validatePassword
from messagebox import messageBox

#todo: fix: dodać main

class Ui_IForgot(object):

    def __init__(self):
        Dialog = QtWidgets.QDialog()
        self.Dialog = Dialog
        self.setupUi(Dialog)
        self.Dialog.show()
        self.Dialog.exec()

        # DB
        self.db = Database()
        self.db.connect()

    def initProcess(self):
        email = self.lineEdit.text()

        if(validateEmail(email)):
            if(self.checkEmailInDB(email)):
                token = str(uuid4())
                self.addTokenToDB(email, token)
                self.sendMail(email, token)
            else:
                messageBox("Reset hasła nie powiódł się", QtWidgets.QMessageBox.Warning, "Tego adresu e-mail nie ma w systemie.")
        else:
            messageBox("Reset hasła nie powiódł się", QtWidgets.QMessageBox.Warning, "Niewłaściwy email. Adres musi zawierać znaki @ i .")
    
    def changePassword(self):
        token = self.lineEdit_2.text()
        new_pass = self.lineEdit_3.text()

        if(validatePassword(new_pass)):
            
            result = self.db.fetchone(f"SELECT COUNT(*) FROM uzytkownicy WHERE reset_token = \'{token}\'") # query
            if result != 0:
                self.db.execute(f"UPDATE uzytkownicy SET haslo = \'{hashlib.md5(new_pass.encode('utf-8')).hexdigest()}\' WHERE reset_token = \'{token}\'") # zmień hasło
                self.db.execute(f"UPDATE uzytkownicy SET reset_token = NULL WHERE reset_token = \'{token}\'") # usuń token po wykorzystaniu
                messageBox("Reset hasła pomyślny", QtWidgets.QMessageBox.Information, "Twoje hasło zostało zresetowane.")
                self.Dialog.close()
            else:
                messageBox("Reset hasła nie powiódł się", QtWidgets.QMessageBox.Warning, "Niewłaściwy token. Spróbuj ponownie.")
        else:
            messageBox("Reset hasła nie powiódł się", QtWidgets.QMessageBox.Warning, "Niewłaściwe hasło. Hasło musi mieć minimum 8 znaków.")


    def show_hide(self):
        
        self.Dialog.resize(451, 250)
        self.frame.hide()
        self.frame_2.show()
        self.frame_2.raise_()

    def checkEmailInDB(self, email):
        result = self.db.fetchone(f"SELECT COUNT(*) FROM uzytkownicy WHERE email = \'{email}\'") # query
        if result == 1:
            return True
        else:
            return False

    def addTokenToDB(self, email, token):
        self.db.execute(f"UPDATE uzytkownicy SET reset_token = \'{token}\' WHERE email = \'{email}\'") # query

    def sendMail(self, email, token):

        port = 587  # For SSL
        smtp_server = "smtp.gmail.com" # iCloud: smtp.mail.me.com
        sender_email = "kogachix@gmail.com"  # Enter your address
        receiver_email = email
        with open('base/email_pass.txt', 'r') as f:
            password = f.readline()
        message = f"From: kogachix@gmail.com\r\nTo: {receiver_email}\r\nSubject: Twój token odzyskiwania do aplikacji Dziennik\r\n\r\nHej {receiver_email}, oto twój token do odzyskania hasła do aplikacji Dziennik:\r\n {token}\r\nJeśli nie prosiłeś (-aś) o zmianę hasła, zignoruj tą wiadomość.".encode('utf-8')

        try:
            context = ssl.create_default_context()
            with smtplib.SMTP(smtp_server, port) as server:
                server.ehlo()  # Can be omitted
                server.starttls(context=context)
                server.ehlo()  # Can be omitted
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message)
                self.show_hide()
            messageBox("Informacja", QtWidgets.QMessageBox.Information, "Na twój adres e-mail został wysłany token. Sprawdź swoją skrzynkę.")
        except Exception:
            messageBox("Błąd systemu", QtWidgets.QMessageBox.Critical, "Połączenie z serwerem e-mail nie działa.")

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(451, 191)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(80, 0, 291, 51))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(10, 70, 431, 381))
        self.widget.setObjectName("widget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.frame = QtWidgets.QFrame(self.widget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.widget1 = QtWidgets.QWidget(self.frame)
        self.widget1.setGeometry(QtCore.QRect(0, 0, 421, 91))
        self.widget1.setObjectName("widget1")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget1)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(self.widget1)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.lineEdit = QtWidgets.QLineEdit(self.widget1)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)
        self.pushButton = QtWidgets.QPushButton(self.widget1)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.verticalLayout_3.addWidget(self.frame)
        self.frame_2 = QtWidgets.QFrame(self.widget)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.widget2 = QtWidgets.QWidget(self.frame_2)
        self.widget2.setGeometry(QtCore.QRect(0, 0, 421, 161))
        self.widget2.setObjectName("widget2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.widget2)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.widget2)
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.verticalLayout_2.addWidget(self.lineEdit_2)
        self.label_4 = QtWidgets.QLabel(self.widget2)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_2.addWidget(self.label_4)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.widget2)
        self.lineEdit_3.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.verticalLayout_2.addWidget(self.lineEdit_3)
        self.pushButton_2 = QtWidgets.QPushButton(self.widget2)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_2.addWidget(self.pushButton_2)
        self.verticalLayout_3.addWidget(self.frame_2)

        self.pushButton.clicked.connect(self.initProcess)
        self.pushButton_2.clicked.connect(self.changePassword)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Zapomniałem hasła"))
        self.label.setText(_translate("Dialog", "Zapomniałem hasła"))
        self.label_2.setText(_translate("Dialog", "Adres e-mail"))
        self.pushButton.setText(_translate("Dialog", "Przypomnij hasło"))
        self.label_3.setText(_translate("Dialog", "Podaj token"))
        self.label_4.setText(_translate("Dialog", "Podaj nowe hasło"))
        self.pushButton_2.setText(_translate("Dialog", "Zmień hasło"))

