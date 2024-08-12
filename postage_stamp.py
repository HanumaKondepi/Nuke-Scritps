'''
This script will create postage stamp from the clipboard
'''

from PySide2 import QtGui
import re

clipboard = QtGui.QGuiApplication.clipboard()
clipboard_data = clipboard.text()

file_paths = re.findall(r'file (.+)', clipboard_data)
names = re.findall(r'name (.+)', clipboard_data)

x = get_pos()[0]
y = get_pos()[1]

#get x and y position of where to paste
def get_pos():
    temp_node = nuke.createNode("Dot", inpanel = False)
    x = temp_node.xpos()
    y = temp_node.ypos()
    nuke.delete(temp_node)
    return x, y

#create postage stamp from the nodes copied to clipboard
def create_postage():
    global x
    global y
    files = []
    for name in names:
        source_node = nuke.toNode(name)
        postage = nuke.nodes.PostageStamp(xpos = x, ypos = y)
        postage["hide_input"].setValue(1)
        postage["postage_stamp"].setValue(1)
        postage.setInput(0, source_node)
        #increment x pos value 150 to add gap between nodes
        x += 150


'''to run the script
copy this file to scripts folder already added to init.py and add following command to menu.py

nuke.menu( 'Nuke' ).addCommand( 'Utilities/Script/postage stamp from clipboard' , 'import postage_stamp ; postage_stamp.create_postage()', 'ctrl+shift+v', shortcutContext = 2)

'''
