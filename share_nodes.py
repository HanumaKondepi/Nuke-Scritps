'''
Script Written by Hanuma
Dt: 09/07/2024
For: The Mill
'''

from PySide2.QtWidgets import QLineEdit, QWidget, QCompleter, QPushButton, QListWidget, QListWidgetItem, QLabel, \
    QApplication, QVBoxLayout, QHBoxLayout, QMessageBox, QComboBox
from PySide2 import QtWidgets
from PySide2.QtCore import Qt
from PySide2.QtGui import QFont
import os
import nuke
import getpass
import time


"""
Change file_sharedir variable to define the folder where all the shared nuke nodes are saved
Change users_list variable to add the list of users available in the domain, if not availabe ask the users to create one folder in any specified path same as thier username 
"""
file_sharedir = "/jobs/tvcResources/bangComms/Mill_IndiaTools/shares"
users_list = os.listdir("/usr/people")
sys_user = getpass.getuser()
shared_dir = os.path.join(file_sharedir, sys_user) + "/"
shared_sets = os.listdir(shared_dir)


class ShareNodes_Copy(QtWidgets.QWidget):
    def __init__(self, parent = QtWidgets.QApplication.activeWindow()):
        super(ShareNodes_Copy, self).__init__()
        self.setWindowTitle("Share Nodes")
        self.resize(400, 450)
        self.setMinimumWidth(300)
        self.setMinimumHeight(450)
        self.setMaximumWidth(400)
        global users_list

        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(True)
        self.enteuser_label = QLabel("Enter User Name:")
        self.enteuser_label.setFont(font)

        self.enter_user = QLineEdit()
        self.enter_user.setToolTip(
            "enter the user name of the artist you would like to share the nodes with \n autocomplete will help you to pick the user name")
        self.enter_user.setMinimumWidth(50)
        self.enter_user.setMinimumHeight(25)

        self.completer = QCompleter(users_list)
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.completer.setFilterMode(Qt.MatchFlag.MatchContains)
        self.completer.setWidget(self.enter_user)
        self.completer.activated.connect(self.handleCompletion)
        self.enter_user.textChanged.connect(self.handleTextChanged)
        self._completing = False

        # add user button
        self.add_user = QPushButton("Add User")
        self.add_user.setMinimumHeight(50)
        self.add_user.setToolTip(
            "This will add the user you selected to the list of users, \n you can share the nodes with multiple users at the same time")
        self.add_user.clicked.connect(self.add)
        self.add_user.setFont(font)

        self.selu_label = QLabel("selected Users List:")
        self.selu_label.setFont(font)

        self.selected_users = QListWidget()
        self.selected_users.setToolTip("Users you have selected you can uncheck the user to skip sharing")

        self.nodeset_lable = QLabel("Nuke File Name:")
        self.nodeset_lable.setFont(font)

        self.name_nodeset = QLineEdit()
        self.name_nodeset.setMinimumWidth(250)
        self.name_nodeset.setMinimumHeight(25)
        self.name_nodeset.setToolTip("enter a name to share the nodes")

        self.share_nodeset = QPushButton("Share Toolset")
        self.share_nodeset.setMinimumWidth(150)
        self.share_nodeset.setMinimumHeight(75)
        self.share_nodeset.setFont(font)
        self.share_nodeset.clicked.connect(self.shared_nodes)

        self.msg = QMessageBox()

        # Add QT Widgets to the Rows
        master_Layout = QVBoxLayout()

        row1 = QHBoxLayout()
        row1.addWidget(self.enteuser_label, alignment=Qt.AlignLeft)

        row2 = QHBoxLayout()
        row2.addWidget(self.enter_user, alignment=Qt.AlignLeft)
        row2.addWidget(self.add_user, alignment=Qt.AlignCenter)

        row3 = QHBoxLayout()
        row3.addWidget(self.selu_label, alignment=Qt.AlignLeft)

        row4 = QHBoxLayout()
        row4.addWidget(self.selected_users)

        row5 = QHBoxLayout()
        row5.addWidget(self.nodeset_lable, alignment=Qt.AlignLeft)

        row6 = QHBoxLayout()
        row6.addWidget(self.name_nodeset)

        row7 = QHBoxLayout()
        row7.addWidget(self.share_nodeset, alignment=Qt.AlignRight)

        master_Layout.addLayout(row1)
        master_Layout.addLayout(row2)
        master_Layout.addLayout(row3)
        master_Layout.addLayout(row4)
        master_Layout.addLayout(row5)
        master_Layout.addLayout(row6)
        master_Layout.addLayout(row7)

        self.setLayout(master_Layout)

    def search_enable(self):
        search_state = self.search_check.isChecked()
        if search_state == 1:
            self.search_key.setHidden(0)
            self.search_button.setHidden(0)
            self.found_users.setHidden(0)
        else:
            self.search_key.setHidden(1)
            self.search_button.setHidden(1)
            self.found_users.setHidden(1)

    def add(self):
        global users_list
        user = self.enter_user.text()
        if len(user) > 0:
            for u in users_list:
                if user == u:
                    new_user = QListWidgetItem(u)
                    new_user.setFlags(new_user.flags() | Qt.ItemIsUserCheckable)
                    new_user.setCheckState(Qt.Checked)
                    self.selected_users.addItem(new_user)
                    self.enter_user.clear()
        else:
            self.msg.setWindowTitle("Error")
            self.msg.setText("Please add a user name")
            self.msg.setIcon(QMessageBox.Warning)
            x = self.msg.exec_()

    def handleTextChanged(self, text):
        if not self._completing:
            found = False
            prefix = text.rpartition(',')[-1]
            if len(prefix) > 1:
                self.completer.setCompletionPrefix(prefix)
                if self.completer.currentRow() >= 0:
                    found = True
            if found:
                self.completer.complete()
            else:
                self.completer.popup().hide()

    def handleCompletion(self, text):
        if not self._completing:
            self._completing = True
            prefix = self.completer.completionPrefix()
            self.enter_user.setText(self.enter_user.text()[:-len(prefix)] + text)
            self._completing = False

    def shared_nodes(self):
        n_selusrs = range(self.selected_users.count())
        if len(n_selusrs) > 0:
            global file_sharedir
            global sys_user
            #nodes = nuke.selectedNodes()
            share_name_t = (self.name_nodeset.text()).lower()
            # Remove all spaces from the sharing name
            share_name = ""
            for a in share_name_t:
                if a == " ":
                    b = "_"
                    share_name += b
                else:
                    share_name += a
            if len(share_name) >= 1:
                for i in range(self.selected_users.count()):
                    s_user_t = self.selected_users.item(i)
                    s_user = s_user_t.text()
                    nuke_file = "/" + sys_user + "_" + share_name + ".nk"
                    share_path = file_sharedir + "/" + s_user
                    if not os.path.isdir(share_path):
                        os.makedirs(share_path)
                    final_name = share_path + nuke_file
                    if s_user_t.checkState():
                        nuke.nodeCopy(final_name)
                self.selected_users.clear()
                self.name_nodeset.clear()
                self.success()

            else:
                self.msg.setWindowTitle("Error")
                self.msg.setText("Please enter a name for fileset")
                self.msg.setIcon(QMessageBox.Warning)
                x = msg.exec_()
        else:
            self.msg.setWindowTitle("Error")
            self.msg.setText("Please select users to share")
            self.msg.setIcon(QMessageBox.Warning)
            x = self.msg.exec_()

    def success(self):
        self.msg.setWindowTitle("Success")
        self.msg.setText("Shared with the User succesfully \n please note all the files shared will be auto deleted after 14days")
        self.msg.setIcon(QMessageBox.Information)

        self.msg.buttonClicked.connect(self.closeWindow)
        x = self.msg.exec_()

    def closeWindow(self):
        self.close()


class ShareNodes_Paste(QtWidgets.QWidget):
    def __init__(self):
        super(ShareNodes_Paste, self).__init__()
        self.setWindowTitle("Get Nodes")
        #self.resize(400, 200)
        self.setMinimumWidth(200)
        #self.setMinimumHeight(200)
        self.setMaximumWidth(200)
        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(True)
        global file_sharedir
        global sys_user
        global shared_dir
        global shared_sets



        self.label = QLabel()
        self.label.setText("Get Nodes:")
        self.label.setFont(font)

        self.combobox1 = QComboBox()
        self.combobox1.addItems(shared_sets)

        self.ok1 = QPushButton()
        self.ok1.setText("Get Nodes")
        self.ok1.clicked.connect(self.clicked)



        row1 = QHBoxLayout()
        row1.addWidget(self.label, alignment=Qt.AlignLeft)
        row2 = QHBoxLayout()
        row2.addWidget(self.combobox1, alignment=Qt.AlignLeft)
        row3 = QHBoxLayout()
        row3.addWidget(self.ok1, alignment=Qt.AlignRight)

        main_layout = QVBoxLayout()

        main_layout.addLayout(row1)
        main_layout.addLayout(row2)
        main_layout.addLayout(row3)
        self.setLayout(main_layout)

    def clicked(self):
        global shared_dir
        file_name = self.combobox1.currentText()
        path = shared_dir + "/" + file_name
        self.delete_old()
        nuke.nodePaste(path)
        self.closeWindow()

    def closeWindow(self):
        self.close()
		

    # get the time
    def getTnM(self, file_time):
        f_time = time.ctime(file_time)
        f_obj = time.strptime(f_time)
        f_date = time.strftime("%Y%m%d", f_obj)
        return f_date

        
    def delete_old(self):
        global shared_dir
        global shared_sets
        for fl in shared_sets:            
            file_path = shared_dir + fl
            file_time = os.path.getmtime(file_path)

            # get the created date to delete
            f_m = int(self.getTnM(file_time))
            c_m = int(self.getTnM(time.time()))
            if c_m-f_m > 14:
                os.remove(file_path)


copy_nodes = ShareNodes_Copy()
paste_nodes = ShareNodes_Paste()
