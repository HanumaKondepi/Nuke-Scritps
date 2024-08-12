"""
@script: Project Folder Structure Creator
@version: V01
@script writer: Hanuma Kondepi

This script is inspired from the folder structure of The Mill (Legacy MPC) Pipeline
And I would like to declare I didn't get any source code of the original script,
and I've written based on my working experience while I was part of The Mill
"""

from PySide2.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, \
    QCheckBox, QApplication, QLineEdit, QGridLayout, QTableWidget, QTableWidgetItem, QMessageBox
from PySide2.QtCore import Qt
from PySide2.QtGui import QIntValidator, QFont
import os


class ProjectDirBuilder(QWidget):
    def __init__(self):
        super(ProjectDirBuilder, self).__init__()
        self.setWindowTitle("Project Structure Builder")
        self.setMinimumWidth(650)
        self.setMaximumWidth(650)

        self.project_dirs = ["archive", "build", "common", "config", "design", "docs", "editorial", "library",
                             "stock_elements", "previs", "reference", "rnd", "templates", "tools", "misc"]
        self.shot_dirs = ["AE", "C4D", "comp", "DMP", "elements", "houdini", "maya", "nuke", "prep", "release", "roto",
                          "tools", "nuke/scripts", "maya/modeling", "maya/texturing", "maya/lookdev", "maya/lighting",
                          "maya/rigging", "maya/animation", "maya/matchmove", "matchmove", "nuke/scripts/roto",
                          "nuke/scripts/prep", "nuke/scripts/comp", "maya/fx"]

        self.tittle_font = QFont()
        self.tittle_font.setBold(True)
        self.tittle_font.setFamily("Arial")
        self.tittle_font.setPointSize(9)

        self.label1 = QLabel("Project Directory:")
        self.label1.setFont(self.tittle_font)

        self.get_folder = QLineEdit()
        self.get_folder.setPlaceholderText("Add Directory Path to Create Project")
        self.get_folder.setMinimumWidth(500)

        self.label2 = QLabel("Project name:")
        self.label2.setFont(self.tittle_font)

        self.project_name = QLineEdit()
        self.project_name.setPlaceholderText("Enter Project Name")
        self.project_name.setMinimumWidth(500)

        self.label3 = QLabel("Add Sequences:")
        self.ask_seq = QCheckBox()
        self.ask_seq.setText("Would you like to add Sequences?")
        self.ask_seq.clicked.connect(self.display_seq)

        self.label4 = QLabel("sequence Name:")
        self.label4.setVisible(0)

        self.sequence_name = QLineEdit()
        self.sequence_name.setPlaceholderText("Enter Sequence Name")
        self.sequence_name.setMaxLength(3)
        self.sequence_name.setMinimumWidth(250)
        self.sequence_name.setVisible(0)

        self.label5 = QLabel("Shot Count:")

        self.no_shots = QLineEdit()
        self.no_shots.setPlaceholderText("No of shots in sequence")
        self.no_shots.setMinimumWidth(250)
        self.no_shots.setValidator(QIntValidator())

        self.label6 = QLabel("Increment:")

        self.no_increment = QLineEdit()
        self.no_increment.setPlaceholderText("Incremental number for each shot")
        self.no_increment.setMinimumWidth(250)
        self.no_increment.setValidator(QIntValidator())


        self.add_sequence = QPushButton("Add Sequence")
        self.add_sequence.setMinimumWidth(125)
        self.add_sequence.setMinimumHeight(50)
        self.add_sequence.setVisible(0)
        self.add_sequence.clicked.connect(self.seq_added)

        self.added_sequences = QTableWidget()
        self.added_sequences.setMaximumHeight(200)
        self.added_sequences.setVisible(0)

        self.create_project = QPushButton("Create Project")
        self.create_project.setMinimumWidth(200)
        self.create_project.setMinimumHeight(100)
        self.create_project.clicked.connect(self.project_create)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setMinimumWidth(100)
        self.cancel_button.setMinimumHeight(50)
        self.cancel_button.clicked.connect(self.close)

        row1 = QHBoxLayout()
        row2 = QHBoxLayout()
        row3 = QHBoxLayout()
        row4 = QHBoxLayout()
        row5 = QHBoxLayout()
        row6 = QHBoxLayout()
        row7 = QHBoxLayout()
        row8 = QHBoxLayout()
        row9 = QHBoxLayout()

        row1.addWidget(self.label1, alignment=Qt.AlignLeft)
        row1.addWidget(self.get_folder, alignment=Qt.AlignRight)

        row2.addWidget(self.label2)
        row2.addWidget(self.project_name, alignment=Qt.AlignRight)

        row3.addWidget(self.ask_seq, alignment=Qt.AlignRight)

        row4.addWidget(self.label4, alignment=Qt.AlignLeft)
        row4.addWidget(self.sequence_name, alignment=Qt.AlignRight)

        row5.addWidget(self.label5, alignment=Qt.AlignLeft)
        row5.addWidget(self.no_shots, alignment=Qt.AlignRight)

        row6.addWidget(self.label6, alignment=Qt.AlignLeft)
        row6.addWidget(self.no_increment, alignment=Qt.AlignRight)

        row7.addWidget(self.add_sequence, alignment=Qt.AlignRight)

        row8.addWidget(self.added_sequences)

        row9.addWidget(self.cancel_button, alignment=Qt.AlignLeft)
        row9.addWidget(self.create_project, alignment=Qt.AlignRight)

        master_layout = QVBoxLayout()
        master_layout.addLayout(row1)
        master_layout.addLayout(row2)
        master_layout.addLayout(row3)
        master_layout.addLayout(row4)
        master_layout.addLayout(row5)
        master_layout.addLayout(row6)
        master_layout.addLayout(row7)
        master_layout.addLayout(row8)
        master_layout.addLayout(row9)

        self.setLayout(master_layout)

        self.mes = QMessageBox()

    def display_seq(self):
        seq_selected = self.ask_seq.isChecked()
        if seq_selected:
            self.setMinimumHeight(450)
            self.setMaximumHeight(450)
            self.sequence_name.setVisible(1)
            self.label4.setVisible(1)
            self.add_sequence.setVisible(1)
            self.added_sequences.setVisible(1)
        else:
            self.setMinimumHeight(250)
            self.setMaximumHeight(250)
            self.sequence_name.setVisible(0)
            self.label4.setVisible(0)
            self.add_sequence.setVisible(0)
            self.added_sequences.setVisible(0)

    def seq_added(self):
        newseq_name = self.sequence_name.text().lower()
        sh_count = self.no_shots.text()
        incr = self.no_increment.text()
        # a small logic to avoid leaving any of the above variables blank
        insert_logic = len(newseq_name) * len(sh_count) * len(incr)
        if insert_logic != 0:
            row_count = self.added_sequences.rowCount()
            self.added_sequences.insertRow(row_count + 1)
            self.added_sequences.setRowCount(row_count + 1)
            self.added_sequences.setColumnCount(3)
            self.added_sequences.setHorizontalHeaderLabels(("Sequence Name", "Number of Shots", "Shot Increment"))
            self.added_sequences.setItem(row_count, 0, QTableWidgetItem(newseq_name))
            self.added_sequences.setItem(row_count, 1, QTableWidgetItem(sh_count))
            self.added_sequences.setItem(row_count, 2, QTableWidgetItem(incr))
            row_count += 1
            self.sequence_name.clear()
            self.no_shots.clear()
            self.no_increment.clear()

    def project_create(self):
        project_dir = self.get_folder.text()
        project_name = self.project_name.text()
        sequences_count = self.added_sequences.rowCount()
        seq_selected = self.ask_seq.isChecked()
        first_logic = len(project_dir) * len(project_name)
        if first_logic != 0 and os.path.exists(project_dir):
            self.proj_folders(project_dir, project_name)
            if seq_selected:
                for sequence in range(sequences_count):
                    sequence_name = self.added_sequences.item(sequence, 0).text()
                    shots_count = int(self.added_sequences.item(sequence, 1).text())
                    incremental_number = int(self.added_sequences.item(sequence, 2).text())
                    incremental_number2 = int(self.added_sequences.item(sequence, 2).text())
                    for shot in range(shots_count):
                        if incremental_number2 < 9:
                            prefix = "_000"
                        elif incremental_number2 < 99:
                            prefix = "_00"
                        elif incremental_number2 < 999:
                            prefix = "_0"
                        else:
                            prefix = "sh_"
                        shot_number = sequence_name + prefix + str(incremental_number2)
                        path = os.path.join(project_dir, project_name, sequence_name, shot_number)
                        os.makedirs(path, exist_ok=True)
                        incremental_number2 += incremental_number
                        self.shot_folders(path)

            else:
                shots_count = int(self.no_shots.text())
                incremental_number = int(self.no_increment.text())
                incremental_number2 = int(self.no_increment.text())
                for shot in range(shots_count):
                    if incremental_number2 < 9:
                        prefix = "sh_000"
                    elif incremental_number2 < 99:
                        prefix = "sh_00"
                    elif incremental_number2 < 999:
                        prefix = "sh_0"
                    else:
                        prefix = "sh_"
                    shot_number = prefix + str(incremental_number2)
                    path = os.path.join(project_dir, project_name, "shots", shot_number)
                    os.makedirs(path, exist_ok=True)
                    incremental_number2 += incremental_number
                    self.shot_folders(path)
            self.success()
        else:
            self.mes.setWindowTitle("error")
            self.mes.setText("Entering a valid Project Directory and Project folder name is mandatory")
            self.mes.setIcon(QMessageBox.Critical)
            x = self.mes.exec_()

    def shot_folders(self, path):
        path = path
        for folder in self.shot_dirs:
            sub_path = os.path.join(path, folder)
            os.makedirs(sub_path, exist_ok=True)

    def proj_folders(self, project_dir, project_name):
        for folder in self.project_dirs:
            f_path = os.path.join(project_dir, project_name, folder)
            os.makedirs(f_path, exist_ok=True)

    def success(self):
        self.mes.setWindowTitle("success")
        self.mes.setText("Successfully Created Project Folders")
        self.mes.setIcon(QMessageBox.Information)
        self.mes.buttonClicked.connect(self.close_window)
        x = self.mes.exec_()

    def close_window(self):
        self.close()


if __name__ in "__main__":
    app = QApplication([])
    main_window = ProjectDirBuilder()
    main_window.show()
    app.exec_()
