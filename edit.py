from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QInputDialog,  QMessageBox, QComboBox, QFileDialog
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
import os
import re
from crontab import CronTab


# Окно добавления репозитория
class EditWindow(object):
    def setupUi(self, Ui_EditWindow):
        Ui_EditWindow.setObjectName("Ui_EditWindow")
        Ui_EditWindow.setFixedSize(600, 410)
        self.cron = CronTab(user=True)
        ### Определяем пакетный менедждер
        os_version = os.popen('lsb_release -a | grep \'Release\'', 'r').read()
        if float(re.search(r'\d.\d', os_version)[0]) < 7.3:
            self.cpm = 'yum'
        elif float(re.search(r'\d.\d', os_version)[0]) >= 7.3:
            self.cpm = 'dnf'
        else: # Не Ред ОС
            exit()
        ###
        self.text_name_value = ''
        self.text_path_value = '/var/www/html/repo/'
        self.repo_id_value = ''
        if os.path.exists("/var/www/html/repo/local_repo.txt"):
            with open('/var/www/html/repo/local_repo.txt', 'r') as file:
                content = file.read()
                self.text_name_value = re.search(r'Репозиторий .* был', content)[0][12:-4]
                self.text_path_value = re.search(r'Путь:.*', content)[0][6:]
                self.repo_id_value = re.search(r'ID Репозитория:.*', content)[0][16:]
                file.close()
        ###
        self.name = QtWidgets.QLabel(Ui_EditWindow)                    
        self.name.setGeometry(QtCore.QRect(40, 10, 520, 40))
        self.name.setStyleSheet("QLabel {\n"
                                "font-size: 24px;\n"
                                "color: red;\n"
                                "}")
        self.name.setObjectName("name")

        self.text_name = QtWidgets.QLineEdit(Ui_EditWindow)                        
        self.text_name.setGeometry(QtCore.QRect(20, 50, 560, 40))
        self.text_name.setStyleSheet("QLineEdit {\n"
                                     "font-size: 24px;\n"
                                     "}")
        self.text_name.setObjectName("text_name")
        self.text_name.setPlaceholderText("Например: redos-7.3")        
        ###
        self.path = QtWidgets.QLabel(Ui_EditWindow) 
        self.path.setGeometry(QtCore.QRect(40, 110, 520, 40))
        self.path.setStyleSheet("QLabel {\n"
                                   "font-size: 24px;\n"
                                   "color: red;\n"
                                   "}")
        self.path.setObjectName("path")

        self.text_path = QtWidgets.QLineEdit(Ui_EditWindow)
        self.text_path.setGeometry(QtCore.QRect(20, 150, 510, 40))
        self.text_path.setStyleSheet("QLineEdit {\n"
                                             "    font-size: 24px;\n"
                                             "}")
        self.text_path.setObjectName("text_path")
        self.text_path.setPlaceholderText("Например: /var/www/html/repo")    
        self.chooseDirectoryButton = QtWidgets.QPushButton(Ui_EditWindow)
        self.chooseDirectoryButton.setGeometry(QtCore.QRect(540, 150, 40, 40))
        self.chooseDirectoryButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.chooseDirectoryButton.setStyleSheet("QPushButton {\n"
                                             "    font-size: 18px;\n"
                                             "    background-color: rgb(255, 69, 69);\n"
                                             "    border: 3px solid rgb(255, 255, 255);\n"
                                             "    color: white;\n"
                                             "    border-radius: 15px;\n"
                                             "}\n"
                                             "QPushButton:hover {\n"
                                             "    background-color: red;\n"
                                             "    border: 3px solid black;\n"
                                             "}")
        self.chooseDirectoryButton.setObjectName("chooseDirectoryButton")
        self.chooseDirectoryButton.clicked.connect(self.getDirectory)

        self.repo_name = QtWidgets.QLabel(Ui_EditWindow)                    
        self.repo_name.setGeometry(QtCore.QRect(40, 200, 520, 40))
        self.repo_name.setStyleSheet("QLabel {\n"
                                     "font-size: 24px;\n"
                                     "color: red;\n"
                                     "}")
        self.repo_name.setObjectName("repo_name")
        self.repo_id = QComboBox(Ui_EditWindow)                    
        self.repo_id.setGeometry(QtCore.QRect(20, 240, 560, 40))
        self.repo_id.setStyleSheet("QComboBox {\n"
                                   "font-size: 24px;\n"
                                   "}")
        self.repo_id.setObjectName("repo_id")
        repo_list = re.findall(r'(?<=\n)\S* ', os.popen(f'{self.cpm} repolist', 'r').read())
        self.repo_id.addItems(repo_list) 

        self.sync_box = QtWidgets.QCheckBox("Авто синхронизация", Ui_EditWindow)                 
        self.sync_box.setGeometry(QtCore.QRect(40, 300, 300, 40))
        self.sync_box.setStyleSheet("QCheckBox {\n"
                                     "font-size: 24px;\n"
                                     "}\n"
                                     "QCheckBox::indicator {\n"
                                     "width: 25px;\n"
                                     "height: 25px;\n"
                                     "}")
        self.sync_box.setObjectName("sync_box")
        self.sync_box.stateChanged.connect(lambda : self.showSyncSettings(Ui_EditWindow))

        self.pushButtonHelp = QtWidgets.QPushButton(Ui_EditWindow)
        self.pushButtonHelp.setGeometry(QtCore.QRect(360, 300, 150, 40))
        self.pushButtonHelp.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButtonHelp.setStyleSheet("QPushButton {\n"
                                             "    font-size: 18px;\n"
                                             "    background-color: rgb(255, 69, 69);\n"
                                             "    border: 3px solid rgb(255, 255, 255);\n"
                                             "    color: white;\n"
                                             "    border-radius: 15px;\n"
                                             "}\n"
                                             "QPushButton:hover {\n"
                                             "    background-color: red;\n"
                                             "    border: 3px solid black;\n"
                                             "}")
        self.pushButtonHelp.setObjectName("pushButtonHelp")
        self.pushButtonHelp.hide()
        self.pushButtonHelp.clicked.connect(self.button_help)

        self.min = QtWidgets.QLabel(Ui_EditWindow)                    
        self.min.setGeometry(QtCore.QRect(20, 350, 104, 40))
        self.min.setAlignment(QtCore.Qt.AlignCenter)
        self.min.setStyleSheet("QLabel {\n"
                                "font-size: 16px;\n"
                                "color: blue;\n"
                                "}")
        self.min.setObjectName("min")

        self.text_min = QtWidgets.QLineEdit(Ui_EditWindow)                        
        self.text_min.setGeometry(QtCore.QRect(20, 390, 104, 40))
        self.text_min.setStyleSheet("QLineEdit {\n"
                                     "font-size: 24px;\n"
                                     "}")
        self.text_min.setObjectName("text_min")
        min_input_validator = QRegExpValidator(QRegExp("[0-9\,\*\/]*"), self.text_min)
        self.text_min.setValidator(min_input_validator)

        self.hour = QtWidgets.QLabel(Ui_EditWindow)                    
        self.hour.setGeometry(QtCore.QRect(134, 350, 104, 40))
        self.hour.setAlignment(QtCore.Qt.AlignCenter)
        self.hour.setStyleSheet("QLabel {\n"
                                "font-size: 16px;\n"
                                "color: blue;\n"
                                "}")
        self.hour.setObjectName("hour")

        self.text_hour = QtWidgets.QLineEdit(Ui_EditWindow)                        
        self.text_hour.setGeometry(QtCore.QRect(134, 390, 104, 40))
        self.text_hour.setStyleSheet("QLineEdit {\n"
                                     "font-size: 24px;\n"
                                     "}")
        self.text_hour.setObjectName("text_hour")
        hour_input_validator = QRegExpValidator(QRegExp("[0-9\,\*\/]*"), self.text_hour)
        self.text_hour.setValidator(hour_input_validator)

        self.day = QtWidgets.QLabel(Ui_EditWindow)                    
        self.day.setGeometry(QtCore.QRect(248, 350, 104, 40))
        self.day.setAlignment(QtCore.Qt.AlignCenter)
        self.day.setStyleSheet("QLabel {\n"
                                "font-size: 16px;\n"
                                "color: blue;\n"
                                "}")
        self.day.setObjectName("day")

        self.text_day = QtWidgets.QLineEdit(Ui_EditWindow)                        
        self.text_day.setGeometry(QtCore.QRect(248, 390, 104, 40))
        self.text_day.setStyleSheet("QLineEdit {\n"
                                     "font-size: 24px;\n"
                                     "}")
        self.text_day.setObjectName("text_day")
        day_input_validator = QRegExpValidator(QRegExp("[0-9\,\*\/]*"), self.text_day)
        self.text_day.setValidator(day_input_validator)

        self.month = QtWidgets.QLabel(Ui_EditWindow)                    
        self.month.setGeometry(QtCore.QRect(362, 350, 104, 40))
        self.month.setAlignment(QtCore.Qt.AlignCenter)
        self.month.setStyleSheet("QLabel {\n"
                                "font-size: 16px;\n"
                                "color: blue;\n"
                                "}")
        self.month.setObjectName("month")

        self.text_month = QtWidgets.QLineEdit(Ui_EditWindow)                        
        self.text_month.setGeometry(QtCore.QRect(362, 390, 104, 40))
        self.text_month.setStyleSheet("QLineEdit {\n"
                                     "font-size: 24px;\n"
                                     "}")
        self.text_month.setObjectName("text_month")
        month_input_validator = QRegExpValidator(QRegExp("[0-9\,\*\/]*"), self.text_month)
        self.text_month.setValidator(month_input_validator)

        self.day_of_week = QtWidgets.QLabel(Ui_EditWindow)                    
        self.day_of_week.setGeometry(QtCore.QRect(476, 350, 104, 40))
        self.day_of_week.setAlignment(QtCore.Qt.AlignCenter)
        self.day_of_week.setStyleSheet("QLabel {\n"
                                "font-size: 12px;\n"
                                "color: blue;\n"
                                "}")
        self.day_of_week.setObjectName("day_of_week")

        self.text_day_of_week = QtWidgets.QLineEdit(Ui_EditWindow)                        
        self.text_day_of_week.setGeometry(QtCore.QRect(476, 390, 104, 40))
        self.text_day_of_week.setStyleSheet("QLineEdit {\n"
                                     "font-size: 24px;\n"
                                     "}")
        self.text_day_of_week.setObjectName("text_day_of_week")
        day_of_week_input_validator = QRegExpValidator(QRegExp("[0-9\,\*\/]*"), self.text_day_of_week)
        self.text_day_of_week.setValidator(day_of_week_input_validator)
        ###
        self.pushButtonSave = QtWidgets.QPushButton(Ui_EditWindow)
        self.pushButtonSave.setGeometry(QtCore.QRect(50, 350, 190, 50))
        self.pushButtonSave.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButtonSave.setStyleSheet("QPushButton {\n"
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
        self.pushButtonSave.setObjectName("pushButtonSave")
        self.pushButtonSave.clicked.connect(self.button_save)
        
        self.pushButtonDelete = QtWidgets.QPushButton(Ui_EditWindow)
        self.pushButtonDelete.setGeometry(QtCore.QRect(360, 350, 190, 50))
        self.pushButtonDelete.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButtonDelete.setStyleSheet("QPushButton {\n"
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
        self.pushButtonDelete.setObjectName("pushButtonDelete")
        self.pushButtonDelete.clicked.connect(self.button_delete)

        ###
        self.retranslateUi(Ui_EditWindow)
        QtCore.QMetaObject.connectSlotsByName(Ui_EditWindow)                      

    def retranslateUi(self, Ui_EditWindow):
        _translate = QtCore.QCoreApplication.translate
        Ui_EditWindow.setWindowTitle(_translate("Ui_EditWindow", "Добавление репозитория"))
        self.name.setText(_translate("name", "Имя"))
        self.path.setText(_translate("path", "Путь"))
        self.repo_name.setText(_translate("repo_name", "Привязанный репозиторий"))
        self.pushButtonHelp.setText(_translate("pushButtonHelp", "Помощь"))
        self.min.setText(_translate("min", "Минута"))
        self.hour.setText(_translate("hour", "Час"))
        self.day.setText(_translate("day", "День"))
        self.month.setText(_translate("month", "Месяц"))
        self.day_of_week.setText(_translate("day_of_week", "День недели"))
        self.pushButtonSave.setText(_translate("pushButtonSave", "Сохранить"))
        self.pushButtonDelete.setText(_translate("pushButtonDelete", "Удалить"))
        self.text_name.setText(_translate("text_name", f"{self.text_name_value}"))
        self.text_path.setText(_translate("text_path", f"{self.text_path_value}"))
        self.min.hide()
        self.hour.hide()
        self.day.hide()
        self.month.hide()
        self.day_of_week.hide()
        self.text_min.hide()
        self.text_hour.hide()
        self.text_day.hide()
        self.text_month.hide()
        self.text_day_of_week.hide()
        self.pushButtonHelp.hide()


    def button_save(self):  # Сохранение репозитория
        name = self.text_name.text()
        path = self.text_path.text()
        repo = self.repo_id.currentText()
        msg = QMessageBox()
        msg.setWindowTitle('Уведомление')
        with open(f'local_repo.txt', mode='w', encoding='utf8') as file:
            file.write(f'Репозиторий {name} был создан с помощью программы LocalRepo RedOS\n\
ID Репозитория: {repo}\n\
Путь: {path}')
            file.close()
        if not os.path.exists("/var/www/html/repo/"):
            os.popen(f'mkdir -p /var/www/html/repo')
        os.popen(f'mv local_repo.txt /var/www/html/repo')
        if not os.path.exists(f"{path}/{name}/{repo}"):
            os.popen(f'mkdir -p {path}/{name}/{repo}')
        os.popen(f'ln -s {path}/{name}/{repo} /var/www/html/repo')
        if os.path.exists(f"{self.text_path_value}/{self.text_name_value}/{self.repo_id_value}") and not f"{self.text_path_value}/{self.text_name_value}/{self.repo_id_value}" == f"{path}/{name}/{repo}" and not self.text_name_value == '' and not self.repo_id_value == '':         
            os.popen(f'mv {self.text_path_value}/{self.text_name_value}/{self.repo_id_value} {path}/{name}/{repo}')
        for job in self.cron:
                if job.comment == 'LocalRepo':
                    self.cron.remove(job)
        if self.sync_box.isChecked():
            self.job = self.cron.new(command=f'reposync --download_path={path}/{name} --repoid=base7.3c --downloadcomps --download-metadata && createrepo -v {path}/{name}/{repo} -g comps.xml', comment='LocalRepo')
            self.job.setall(f'{self.text_min.text()}', f'{self.text_hour.text()}', 
                f'{self.text_day.text()}', f'{self.text_month.text()}', f'{self.text_day_of_week.text()}')
        self.cron.write()
        message = 'Сохранение прошло успешно'
        msg.setText(f'{message}')
        msg.exec_()
        if not (self.text_name_value == name):
            #self.button_delete()
            pass


    def button_help(self):  # Окно с подсказкой
        msg = QMessageBox()
        msg.setWindowTitle('Помощь с автосинхронизацией')
        msg.setText("Автосинхронизация организована с помощью планировщика задач Cron.\n\
C помощью 5 окон ввода, вы можете указать время, когда вы хотите выполнять \
синхронизацию локального репозитория. Формат вводимых данных целые числа.\n\
Так же вы можете использовать спец. символы:\n '*' - каждый, например можно поставить \
в графу день, и синхронизация будет происходить каждый день\
\n '/n' - число кратное n, например если указана в графе час, то синхронизация \
будет происходить через каждые n часов\n ',' - через запятую можно указать несколь значений")
        msg.exec_()

    def button_delete(self):  # Удаление репозитория
        name = self.text_name_value
        path = self.text_path_value
        msg = QMessageBox()
        msg.setWindowTitle('Уведомление')
        if os.path.exists("/var/www/html/repo/local_repo.txt"):
            os.popen(f'rm -f /var/www/html/repo/local_repo.txt')
        if os.path.exists(f"{path}{name}"):
            os.popen(f'rm -rf {path}{name}')
        self.text_name.clear()
        self.text_path.clear()
        self.repo_id.clear()
        for job in self.cron:
            if job.comment == 'LocalRepo':
                self.cron.remove(job)


    def getDirectory(self):
        _translate = QtCore.QCoreApplication.translate                                                     
        dirlist = QFileDialog.getExistingDirectory(self,"Выбрать директорию",".")
        self.text_path.setText(_translate("text_path", f"{dirlist}"))

    def showSyncSettings(self, Ui_EditWindow):
        if self.sync_box.isChecked():
            Ui_EditWindow.setFixedSize(600, 510)
            self.pushButtonSave.setGeometry(QtCore.QRect(50, 445, 190, 50))
            self.pushButtonDelete.setGeometry(QtCore.QRect(360, 445, 190, 50))
            self.min.show()
            self.hour.show()
            self.day.show()
            self.month.show()
            self.day_of_week.show()
            self.text_min.show()
            self.text_hour.show()
            self.text_day.show()
            self.text_month.show()
            self.text_day_of_week.show()
            self.pushButtonHelp.show()
        else:
            Ui_EditWindow.setFixedSize(600, 410)
            self.pushButtonSave.setGeometry(QtCore.QRect(50, 350, 190, 50))
            self.pushButtonDelete.setGeometry(QtCore.QRect(360, 350, 190, 50))
            self.min.hide()
            self.hour.hide()
            self.day.hide()
            self.month.hide()
            self.day_of_week.hide()
            self.text_min.hide()
            self.text_hour.hide()
            self.text_day.hide()
            self.text_month.hide()
            self.text_day_of_week.hide()
            self.pushButtonHelp.hide()

        