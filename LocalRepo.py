#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Автор
# Ившин Егор Михайлович
# Cтудент УдГУ института ИПСУБ
# Безопасность Информационных технологий 3 курс
# Версия 1.0

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QMessageBox, QInputDialog, QLineEdit, QTextEdit
from PyQt5.QtCore import QObject, QThread
from PyQt5.QtCore import pyqtSignal as Signal
from edit import EditWindow
import subprocess
import os
import re
import asyncio


def sudo_is_true(password):
    answer = os.popen(f'echo {password} | sudo -S echo "hello"').read().strip()
    return answer == 'hello'

class MyThread(QThread):
    line_printed = Signal(str)

    def __init__(self, parent):
        super(MyThread, self).__init__(parent)
        self.cmd = None

    def start_command(self, cmd):
        self.cmd = cmd
        self.start()

    def run(self):
        if self.cmd:
            popen = subprocess.Popen(self.cmd, stdout=subprocess.PIPE, shell=True)
            lines_iterator = iter(popen.stdout.readline, b"")     

            num = 0
            try:
                for line in lines_iterator:
                    num += 1
                    self.line_printed.emit(line.decode('utf-8', errors='ignore') )
                else:
                    if num == 0:
                        self.line_printed.emit("\n`{}` <<--не является внутренней "
                                               "или внешней командой, \n\tисполняемой "
                                               "программой или пакетным файлом.\n".format(self.cmd))
                    else:
                        self.line_printed.emit("\n{}\n".format("-"*50)) 
            except Exception as e:
                # На случай возникновения какой-нибудь ОШИБКИ 
                self.line_printed.emit("\nException as e: --->{}\n".format(e))                 
        else:
            self.line_printed.emit("\nВы не ввели команду для выполнения Cmd!\n")   


class MyEditWindow(QtWidgets.QWidget, EditWindow):                          
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.authorization()
        self.setting()
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(600, 310)
        MainWindow.setFocusPolicy(QtCore.Qt.ClickFocus)
        MainWindow.setStyleSheet("")
        ### фон
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("background-color: rgb(227, 227, 227);")
        self.centralwidget.setObjectName("centralwidget")

        self.name = QtWidgets.QLabel(self.centralwidget)                    
        self.name.setGeometry(QtCore.QRect(100, 10, 400, 40))
        self.name.setAlignment(QtCore.Qt.AlignCenter) 

        self.name.setStyleSheet("QLabel {\n"
        						"text-align: center;\n"
                                "font-size: 24px;\n"
                                "color: red;\n"
                                "}")
        self.name.setObjectName("name")

        self.version = QtWidgets.QLabel(self.centralwidget)                    
        self.version.setGeometry(QtCore.QRect(20, 60, 560, 40))
        self.version.setStyleSheet("QLabel {\n"
                                   "font-size: 24px;\n"
                                   "}")
        self.version.setObjectName("version")

        self.packets = QtWidgets.QLabel(self.centralwidget)                    
        self.packets.setGeometry(QtCore.QRect(20, 110, 560, 40))
        self.packets.setStyleSheet("QLabel {\n"
                                   "font-size: 24px;\n"
                                   "}")
        self.packets.setObjectName("packets")

        self.volume = QtWidgets.QLabel(self.centralwidget)                    
        self.volume.setGeometry(QtCore.QRect(20, 160, 560, 40))
        self.volume.setStyleSheet("QLabel {\n"
                                  "font-size: 24px;\n"
                                  "}")
        self.volume.setObjectName("volume")

     	### Layout для кнопок
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 230, 600, 50))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.pushButtonEdit = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonEdit.sizePolicy().hasHeightForWidth())
        self.pushButtonEdit.setSizePolicy(sizePolicy)
        self.pushButtonEdit.setBaseSize(QtCore.QSize(0, 0))
        self.pushButtonEdit.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButtonEdit.setStyleSheet("QPushButton {\n"
                                             "    height: 80px;\n"
                                             "    width: 240px;\n"
                                             "    font-size: 28px;\n"
                                             "    background-color: rgb(255, 69, 69);\n"
                                             "    border: 4px solid rgb(255, 255, 255);\n"
                                             "    color: white;\n"
                                             "    border-radius: 15px;\n"
                                             "}\n"
                                             "QPushButton:hover {\n"
                                             "    background-color: red;\n"
                                             "    border: 4px solid black;\n"
                                             "}")
        self.pushButtonEdit.setObjectName("pushButtonAdd")
        self.pushButtonEdit.clicked.connect(self.button_edit)
        self.horizontalLayout.addWidget(self.pushButtonEdit, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.pushButtonSyncronization = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButtonSyncronization.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButtonSyncronization.setStyleSheet("QPushButton {\n"
                                            "    height: 80px;\n"
                                            "    width: 240px;\n"
                                            "    font-size: 24px;\n"
                                            "    background-color: rgb(255, 69, 69);\n"
                                            "    border: 4px solid rgb(255, 255, 255);\n"
                                            "    color: white;\n"
                                            "    border-radius: 15px;\n"
                                            "}\n"
                                            "QPushButton:hover {\n"
                                            "    background-color: red;\n"
                                            "    border: 4px solid black;\n"
                                            "}")
        self.pushButtonSyncronization.setObjectName("pushButtonSyncronization")
        self.pushButtonSyncronization.clicked.connect(self.button_syncronization)
        self.horizontalLayout.addWidget(self.pushButtonSyncronization, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        MainWindow.setCentralWidget(self.centralwidget)
        ###
        self.pushButtonShell = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonShell.setGeometry(QtCore.QRect(0, 300, 600, 10))
        self.pushButtonShell.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButtonShell.setStyleSheet("QPushButton {\n"
                                             "    font-size: 8px;\n"
                                             "    background-color: rgb(255, 69, 69);\n"
                                             "    border: 2px solid rgb(255, 255, 255);\n"
                                             "    color: white;\n"
                                             "    border-radius: 15px;\n"
                                             "}\n"
                                             "QPushButton:hover {\n"
                                             "    background-color: red;\n"
                                             "    border: 2px solid black;\n"
                                             "}")
        self.pushButtonShell.setObjectName("pushButtonShell")
        self.pushButtonShell.clicked.connect(lambda : self.show_shell(MainWindow))

        self.pushButtonRefresh = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonRefresh.setGeometry(QtCore.QRect(480, 10, 100, 40))
        self.pushButtonRefresh.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButtonRefresh.setStyleSheet("QPushButton {\n"
                                             "    font-size: 18px;\n"
                                             "    background-color: rgb(255, 69, 69);\n"
                                             "    border: 2px solid rgb(255, 255, 255);\n"
                                             "    color: white;\n"
                                             "    border-radius: 15px;\n"
                                             "}\n"
                                             "QPushButton:hover {\n"
                                             "    background-color: red;\n"
                                             "    border: 2px solid black;\n"
                                             "}")
        self.pushButtonRefresh.setObjectName("pushButtonRefresh")
        self.pushButtonRefresh.clicked.connect(lambda : self.refresh(MainWindow))

        self.my_shell = QtWidgets.QTextEdit(self.centralwidget)
        self.my_shell.setGeometry(QtCore.QRect(5, 315, 590, 280))
        self.my_shell.setDisabled(True)
        self.my_shell.setStyleSheet("QTextEdit {\n"
                                             "    font-size: 12px;\n"
                                             "    color: black;\n"
                                             "}\n")
        self.open = False
        self.thread = MyThread(self.centralwidget)
        self.thread.line_printed.connect(self.handle_line)
        ###
        self.repo_info()
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def setting(self):
        response = os.popen('getenforce', 'r').read()
        msg = QMessageBox()
        msg.setWindowTitle('Уведомление')
        if response == 'Enforcing\n':
            os.popen(f'setenforce 0')
            message = 'selinux переведён в режим Permissive'
            msg.setText(f'{message}')
            msg.exec_()    
        with open('/etc/httpd/conf/httpd.conf', 'r') as httpdConf:
        	re.search(r'Options Indexes Includes', httpdConf.read()) == False
        	if re.search(r'Options Indexes Includes', httpdConf.read()) == False:
        		os.popen(f'sed -i "s/Options Indexes FollowSymLinks/Options Indexes Includes/" /etc/httpd/conf/httpd.conf')
        if os.popen(f'systemctl is-active httpd', 'r').read() != 'active\n':
                os.popen(f'systemctl enable httpd --now')
                message = 'Служба httpd включена'
                msg.setText(f'{message}')
                msg.exec_()


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Управление локальным репозиторием Red OS"))
        self.name.setText(_translate("MainWindow", f"{self.text_name}"))
        self.version.setText(_translate("MainWindow", f"Дата обновления: {self.date_of_touch}"))
        self.packets.setText(_translate("MainWindow", f"Количество пакетов: {self.repo_counter}"))
        self.volume.setText(_translate("MainWindow", f"Объём: {self.repo_volume}"))
        self.pushButtonEdit.setText(_translate("MainWindow", "Изменить"))
        self.pushButtonSyncronization.setText(_translate("MainWindow", "Синхронизировать"))
        self.pushButtonShell.setText(_translate("MainWindow", "\\/"))
        self.pushButtonRefresh.setText(_translate("MainWindow", "Обновить"))


    def repo_info(self):
        self.text_name = 'None'
        self.text_path = '' 
        self.text_repo_id = ''
        self.repo_volume = ''
        self.repo_counter = ''
        self.date_of_touch = ''
        if os.path.exists("/var/www/html/repo/local_repo.txt"):
        	with open('/var/www/html/repo/local_repo.txt', 'r') as file: 
        		content = file.read()
        		self.text_name = re.search(r'Репозиторий .* был', content)[0][12:-4]
        		self.text_repo_id = re.search(r'ID Репозитория:.*', content)[0][16:]
        		self.text_path = re.search(r'Путь:.*', content)[0][6:]
        		self.repo_volume = re.search(r'итого .*', os.popen(f'ls -lh {self.text_path}/{self.text_name}/{self.text_repo_id}', 'r').read())[0][6:]
        		self.repo_counter = int(os.popen(f'ls -l {self.text_path}/{self.text_name}/{self.text_repo_id} | wc -l', 'r').read()) - 1
        		self.date_of_touch = os.popen(f'ls -l {self.text_path}/{self.text_name} | grep {self.text_repo_id}', 'r').read()
        		self.date_of_touch = ' '.join(re.search(r'\w{3} \w* \d{2}:\d{2}', self.date_of_touch)[0].split(' ')[::-1])
        		file.close()


    def button_edit(self):  # Добавление репозитория
        self.edit = MyEditWindow()
        self.edit.show()


    def button_syncronization(self):
        name = self.text_name
        path = self.text_path
        repo = self.text_repo_id
        msg = QMessageBox()
        msg.setWindowTitle('Уведомление')
        self.thread.start_command(f'reposync --destdir={path}/{name} --repoid={repo} --downloadcomps --download-metadata && createrepo -v {path}/{name}/{repo} -g comps.xml')
        message = 'Процесс синхронизации успешно запущен'
        msg.setText(f'{message}')
        msg.exec_()    


    def authorization(self):
        self.sudo = False
        if not os.geteuid() == 0:
	        while not sudo_is_true(self.sudo):
	            password, ok = QInputDialog.getText(MainWindow, f"Настройка",
	            "Для корректной работы программы Необходимо ввести пароль пользователя, ваш пользователь должен состоять в группе sudo", QLineEdit.Password)
	            if sudo_is_true(password) == False and ok == True:
	                msg = QMessageBox()
	                msg.setWindowTitle('Ошибка')
	                message = 'Не верный пароль'
	                msg.setText(f'{message}')
	                msg.exec_()
	            elif ok == False:
	                exit()
	            else:
	                os.popen(f'sudo -S python3 LocalRepo.py', 'w').write(f'{password}')
	                exit()


    def handle_line(self, line):
        cursor = self.my_shell.textCursor()
        cursor.movePosition(cursor.End)
        cursor.insertText(line)
        self.my_shell.ensureCursorVisible()

    def show_shell(self, MainWindow):
        if not self.open:
            MainWindow.setFixedSize(600, 600)
            self.open = True
        else:
        	MainWindow.setFixedSize(600, 310)
        	self.open = False

    def refresh(self, MainWindow):
        self.repo_info()
        self.retranslateUi(MainWindow)

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
