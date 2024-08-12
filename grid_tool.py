from PySide2.QtWidgets import QWidget, QApplication, QLabel, QPushButton, QCheckBox, QGridLayout
from PySide2 import QtWidgets
from PySide2 import QtGui, QtCore
import nuke


class GridTools(QtWidgets.QWidget):
    def __init__(self):
        super(GridTools, self).__init__()
        self.setWindowTitle("Grid Tools")
        self.resize(300, 300)
        self.setMinimumSize(300, 300)
        self.setMaximumSize(300, 300)
        self.preferencesNode = nuke.toNode('preferences')

        # Show Grid Check Box
        self.showGrid = QCheckBox()
        self.showGrid.setText("Toggle Grid On/Off")
        if self.check_grid():
            self.showGrid.setChecked(True)
        else:
            self.showGrid.setChecked(False)
        self.showGrid.clicked.connect(self.toggle_grid)


        self.snaptoGrid = QCheckBox()
        self.snaptoGrid.setText("Snap to Grid")
        if self.SnapToGrid_checkstate():
            self.snaptoGrid.setChecked(True)
        else:
            self.snaptoGrid.setChecked(False)
        self.snaptoGrid.clicked.connect(self.toggle_SnapToGrid)

        # push buttons
        self.scaleUp_pushButton = QPushButton()
        self.scaleUp_pushButton.setMinimumSize(100, 100)
        self.scaleUp_pushButton.setText("Scale Up")
        self.scaleUp_pushButton.clicked.connect(self.scale_up)

        self.scaleDown_pushButton = QPushButton()
        self.scaleDown_pushButton.setMinimumSize(100, 100)
        self.scaleDown_pushButton.setText("Scale Down")
        self.scaleDown_pushButton.clicked.connect(self.scale_down)

        self.scaleUpX_pushButton = QPushButton()
        self.scaleUpX_pushButton.setMinimumSize(40, 40)
        self.scaleUpX_pushButton.setText("Scale Up X")
        self.scaleUpX_pushButton.clicked.connect(self.scale_upX)

        self.scaleUpY_pushButton = QPushButton()
        self.scaleUpY_pushButton.setMinimumSize(40, 40)
        self.scaleUpY_pushButton.setText("Scale Up Y")
        self.scaleUpY_pushButton.clicked.connect(self.scale_upY)

        self.scaleDownX_pushButton = QPushButton()
        self.scaleDownX_pushButton.setMinimumSize(40, 40)
        self.scaleDownX_pushButton.setText("Scale Down X")
        self.scaleDownX_pushButton.clicked.connect(self.scale_downX)

        self.scaleDownY_pushButton = QPushButton()
        self.scaleDownY_pushButton.setMinimumSize(40, 40)
        self.scaleDownY_pushButton.setText("Scale Down Y")
        self.scaleDownY_pushButton.clicked.connect(self.scale_downY)


        self.gridLayout = QGridLayout()
        self.gridLayout.addWidget(self.showGrid, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.snaptoGrid, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.scaleUp_pushButton, 2, 0, 2, 1)
        self.gridLayout.addWidget(self.scaleUpX_pushButton, 2, 1, 1, 1)
        self.gridLayout.addWidget(self.scaleUpY_pushButton, 3, 1, 1, 1)
        self.gridLayout.addWidget(self.scaleDown_pushButton, 4, 0, 2, 1)
        self.gridLayout.addWidget(self.scaleDownX_pushButton, 4, 1, 1, 1)        
        self.gridLayout.addWidget(self.scaleDownY_pushButton, 5, 1, 1, 1)


        self.setLayout(self.gridLayout)


    def toggle_grid(self):
        #preferencesNode = nuke.toNode('preferences')
        grid = self.preferencesNode["show_grid"]
        grid_selection = self.showGrid.isChecked()
        if grid_selection:
            grid.setValue(1)
        else:
            grid.setValue(0)

    def toggle_SnapToGrid(self):
        stg = self.preferencesNode["SnapToGrid"]
        stg_selection = self.snaptoGrid.isChecked()
        if stg_selection:
            stg.setValue(1)
        else:
            stg.setValue(0)

    def SnapToGrid_checkstate(self):
        stg_state = self.preferencesNode["SnapToGrid"].value()
        return stg_state

    def check_grid(self):
        gridIsOn = self.preferencesNode["show_grid"].value()
        return gridIsOn

    def scale_up(self):
        grid_width = self.preferencesNode["GridWidth"].value()
        grid_height = self.preferencesNode["GridHeight"].value()
        scale_width = grid_width + 10
        scale_height = grid_height + 10
        self.preferencesNode["GridWidth"].setValue(scale_width)
        self.preferencesNode["GridHeight"].setValue(scale_height)

    def scale_down(self):
        grid_width = self.preferencesNode["GridWidth"].value()
        grid_height = self.preferencesNode["GridHeight"].value()
        scale_width = grid_width - 10
        scale_height = grid_height - 10
        self.preferencesNode["GridWidth"].setValue(scale_width)
        self.preferencesNode["GridHeight"].setValue(scale_height)

    def scale_upX(self):
        grid_width = self.preferencesNode["GridWidth"].value()
        grid_height = self.preferencesNode["GridHeight"].value()
        scale_width = grid_width + 10
        scale_height = grid_height + 0
        self.preferencesNode["GridWidth"].setValue(scale_width)
        self.preferencesNode["GridHeight"].setValue(scale_height)

    def scale_upY(self):
        grid_width = self.preferencesNode["GridWidth"].value()
        grid_height = self.preferencesNode["GridHeight"].value()
        scale_width = grid_width + 0
        scale_height = grid_height + 10
        self.preferencesNode["GridWidth"].setValue(scale_width)
        self.preferencesNode["GridHeight"].setValue(scale_height)

    def scale_downX(self):
        grid_width = self.preferencesNode["GridWidth"].value()
        grid_height = self.preferencesNode["GridHeight"].value()
        scale_width = grid_width - 10
        scale_height = grid_height
        self.preferencesNode["GridWidth"].setValue(scale_width)
        self.preferencesNode["GridHeight"].setValue(scale_height)

    def scale_downY(self):
        grid_width = self.preferencesNode["GridWidth"].value()
        grid_height = self.preferencesNode["GridHeight"].value()
        scale_width = grid_width
        scale_height = grid_height - 10
        self.preferencesNode["GridWidth"].setValue(scale_width)
        self.preferencesNode["GridHeight"].setValue(scale_height)

window = GridTools()



'''
add to menu.py
nuke.menu('Nuke').addCommand('Utilities/Script/Grid/grid_tool', 'import grid_tool;grid_tool.window.show()', 'shift+g')
'''