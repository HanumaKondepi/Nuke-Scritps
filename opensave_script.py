from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import os
import re
import nuke


class OpenSaveScript(QWidget):
    def __init__(self):
        super(OpenSaveScript, self).__init__()
        self.resize(450, 550)
        self.setMinimumSize(QSize(420, 550))
        self.setMaximumSize(QSize(420, 550))
        self.setWindowTitle("Open Save Script")

        self.projectDir = "D:\\Python Scripting\\Test"
        self.projectList = os.listdir("D:\\Python Scripting\\Test")

        self.label_3 = QLabel("Sequence")
        font = QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)

        font1 = QFont()
        font1.setPointSize(12)
        font1.setBold(True)
        font1.setWeight(75)
        self.label_3.setFont(font)

        self.seq_comboBox = QComboBox()
        self.seq_comboBox.setMinimumSize(QSize(300, 25))
        self.seq_comboBox.currentIndexChanged.connect(self.list_shots)

        self.tabWidget = QTabWidget()
        self.save = QWidget()

        self.listWidget = QListWidget(self.save)
        self.listWidget.setGeometry(QRect(10, 10, 371, 250))
        self.listWidget.setMinimumSize(QSize(0, 250))
        self.listWidget.setMaximumSize(QSize(16777215, 250))
        self.listWidget.setFont(font)

        self.pushButton = QPushButton(self.save)
        self.pushButton.setText("Save Script")
        self.pushButton.setGeometry(QRect(290, 280, 91, 41))
        self.pushButton.setFont(font)
        self.pushButton.clicked.connect(self.save_script)
        self.tabWidget.addTab(self.save, "")
        self.open = QWidget()
        self.listWidget_2 = QListWidget(self.open)
        self.listWidget_2.setGeometry(QRect(10, 10, 371, 250))
        self.listWidget_2.setMinimumSize(QSize(0, 250))
        self.listWidget_2.setMaximumSize(QSize(16777215, 250))
        self.listWidget_2.setFont(font)
        
        
        self.pushButton_2 = QPushButton(self.open)
        self.pushButton_2.setText("Open Script")
        self.pushButton_2.setGeometry(QRect(290, 280, 91, 41))
        self.pushButton_2.setFont(font)
        self.pushButton_2.clicked.connect(self.open_script)
        self.tabWidget.addTab(self.open, "")

        self.label = QLabel("Select Project")
        self.label.setFont(font)

        self.project_comboBox = QComboBox()
        self.project_comboBox.setMinimumSize(QSize(300, 25))
        self.project_comboBox.addItem("")
        for project in self.projectList:
            self.project_comboBox.addItem(project)
        self.project_comboBox.currentIndexChanged.connect(self.list_seq)

        self.label_5 = QLabel("Task")
        self.label_5.setFont(font)

        self.task_comboBox = QComboBox()
        self.task_comboBox.setMinimumSize(QSize(300, 25))
        self.task_comboBox.currentIndexChanged.connect(self.list_scripts)
        
        self.label_4 = QLabel("Shot Number")
        self.label_4.setFont(font)

        self.shot_comboBox = QComboBox()
        self.shot_comboBox.setMinimumSize(QSize(300, 25))
        self.shot_comboBox.currentIndexChanged.connect(self.list_taks)
        
        self.pushButton_3 = QPushButton("Cancel")
        self.pushButton_3.setMinimumSize(QSize(75, 40))
        self.pushButton_3.setMaximumSize(QSize(75, 40))
        self.pushButton_3.setFont(font)
        self.pushButton_3.clicked.connect(self.closeWindow)
        
        self.gridLayout = QGridLayout()
        
        self.horizontalLayout01 = QHBoxLayout()
        self.horizontalLayout02 = QHBoxLayout()
        self.horizontalLayout03 = QHBoxLayout()
        self.horizontalLayout04 = QHBoxLayout()
        
        self.horizontalLayout01.addWidget(self.label)
        self.horizontalLayout01.addWidget(self.project_comboBox)
        self.horizontalLayout02.addWidget(self.label_3)
        self.horizontalLayout02.addWidget(self.seq_comboBox)
        self.horizontalLayout03.addWidget(self.label_4)
        self.horizontalLayout03.addWidget(self.shot_comboBox)
        self.horizontalLayout04.addWidget(self.label_5)
        self.horizontalLayout04.addWidget(self.task_comboBox)        
        
        self.gridLayout.addLayout(self.horizontalLayout01, 0, 0, 1, 1)
        self.gridLayout.addLayout(self.horizontalLayout02, 1, 0, 1, 1)
        self.gridLayout.addLayout(self.horizontalLayout03, 2, 0, 1, 1)
        self.gridLayout.addLayout(self.horizontalLayout04, 3, 0, 1, 1)
        self.gridLayout.addWidget(self.tabWidget, 4, 0, 1, 1)
        self.gridLayout.addWidget(self.pushButton_3, 6, 0, 1, 1)

        self.setLayout(self.gridLayout)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.save),
                                  QCoreApplication.translate("OpenSaveScript", "Save", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.open),
                                  QCoreApplication.translate("OpenSaveScript", "Open", None))
        self.tabWidget.setFont(font1)

    def closeWindow(self):
        self.close()

    def list_seq(self):
        self.listWidget.clear()
        self.listWidget_2.clear()
        project = str(self.project_comboBox.currentText())
        seq_dir = os.path.join(self.projectDir, project)
        ignore_list = ['archive', 'build', 'common', 'config', 'design', 'docs', 'editorial', 'library', 'misc',
                       'previs', 'reference', 'rnd', 'stock_elements', 'templates', 'tools']
        seq_list = os.listdir(seq_dir)
        self.seq_comboBox.clear()
        for seq in seq_list:
            if not seq in ignore_list:
                self.seq_comboBox.addItem(seq)

    def list_shots(self):
        self.shot_comboBox.clear()
        project = str(self.project_comboBox.currentText())
        seq = str(self.seq_comboBox.currentText())
        shots_dir = os.path.join(self.projectDir, project, seq)
        shots_list = os.listdir(shots_dir)
        for shot in shots_list:
            self.shot_comboBox.addItem(shot)
        self.listWidget.clear()
        self.listWidget_2.clear()
        self.list_scripts()

    def list_taks(self):
        self.listWidget.clear()
        self.listWidget_2.clear()
        self.task_comboBox.clear()
        self.task_comboBox.addItem("comp")
        self.task_comboBox.addItem("LSC")
        self.task_comboBox.addItem("DMP")
        self.task_comboBox.addItem("paint")
        self.task_comboBox.addItem("roto")
        self.listWidget.clear()
        self.listWidget_2.clear()
        self.list_scripts()


    def save_script(self):
        project = str(self.project_comboBox.currentText())
        seq = str(self.seq_comboBox.currentText())
        shot = str(self.shot_comboBox.currentText())
        task = str(self.task_comboBox.currentText())
        script_path = os.path.join(self.projectDir, project, seq, shot, "nuke", "scripts", task)
        if not os.path.isdir(script_path):
            os.makedirs(script_path)
        nuke_dir = os.listdir(script_path)
        if len(nuke_dir) > 0:
            latest_version = self.get_latest(nuke_dir)[1]
            version = self.increment_version(latest_version)
        else:
            version = "001"
        nuke_fle = seq + "_" + shot + "_" + task + "_v" + version + ".nk"
        nuke_filePath = script_path + "\\" + nuke_fle
        nuke.scriptSaveAs(nuke_filePath)
        self.list_scripts()

    def open_script(self):
        project = str(self.project_comboBox.currentText())
        seq = str(self.seq_comboBox.currentText())
        shot = str(self.shot_comboBox.currentText())
        task = str(self.task_comboBox.currentText())
        script_path = os.path.join(self.projectDir, project, seq, shot, "nuke", "scripts", task)
        if not os.path.isdir(script_path):
            os.makedirs(script_path)
        nuke_dir = os.listdir(script_path)
        scripts = self.listWidget_2.count()
        name = [item.text() for item in self.listWidget_2.selectedItems()]
        script_path = script_path + "\\" + name[0]
        nuke.scriptOpen(script_path)


    def list_scripts(self):
        self.listWidget.clear()
        self.listWidget_2.clear()
        project = str(self.project_comboBox.currentText())
        seq = str(self.seq_comboBox.currentText())
        shot = str(self.shot_comboBox.currentText())
        task = str(self.task_comboBox.currentText())
        script_path = os.path.join(self.projectDir, project, seq, shot, "nuke", "scripts", task)
        if os.path.isdir(script_path):
            scripts_dir = os.listdir(script_path)
            for nk in scripts_dir:
                self.listWidget.addItem(nk)
                self.listWidget_2.addItem(nk)

    def get_latest(self, nukefile_list):
        pattern = r"v(\d{3})"
        latest_version = int(0)
        latest_nukefile = None
        for nukefile in nukefile_list:
            match = re.search(pattern, nukefile)
            version_number = match.group(1)
            v = int(version_number)
            if v > latest_version:
                latest_version = v
                latest_nukefile = nukefile
        return latest_nukefile, version_number

    def increment_version(self, string):
        number = int(string)
        number += 1
        formatted_number = format(number, '03d')
        return formatted_number

window = OpenSaveScript()
window.show()