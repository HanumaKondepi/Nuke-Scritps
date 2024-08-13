import nuke
from PySide2 import QtGui, QtCore
import re


class HijackPaste():
    def __init__(self):
        self.clipboard = QtGui.QGuiApplication.clipboard()  # get clipboard data using pyside2
        self.clipboard_data = self.clipboard.text()  # read clipboard contant as normal text
        self.file_paths = re.findall(r'file (.+)', self.clipboard_data)  # find file paths for all the readnodes
        self.names = re.findall(r'name (.+)', self.clipboard_data)  # find names for all the nodes
        self.read_data = re.findall(r'Read \{[^}]*\}', self.clipboard_data)  # find data of read nodes
        self.pos_data = re.findall(r'PostageStamp \{[^}]*\}', self.clipboard_data)  # find data of postagestamps
        self.file_paths = re.findall(r'file (.+)', self.clipboard_data)

        # create empty list 
        self.read_names = []
        self.pos_names = []

        # get names of all read nodes
        for read_node in self.read_data:
            name = re.findall(r'name (.+)', read_node)
            self.read_names.append(name[0])

        # get names of all postage_stamp nodes
        for postage in self.pos_data:
            name = re.findall(r'name (.+)', postage)
            self.pos_names.append(name[0])

    def hijackpaste(self):
        x = self.get_pos()[0]
        y = self.get_pos()[1]
        if self.check_path():
            self.create_postage(x, y)
            # Regular expression to find and remove blocks starting with Read and ending with }
            read = re.sub(r'Read \{[^}]*\}', '', self.clipboard_data, flags=re.DOTALL)
            read_nodesremoved = read.strip()  # delete all read nodes information from clipboard data
            post = re.sub(r'PostageStamp \{[^}]*\}', '', read_nodesremoved, flags=re.DOTALL)
            post_nodesremoved = post.strip()
            self.clipboard.setText(post_nodesremoved)  # prep modified clipboard data
            nuke.nodePaste('%clipboard%')
        else:
            post = re.sub(r'PostageStamp \{[^}]*\}', '', self.clipboard_data, flags=re.DOTALL)
            post_nodesremoved = post.strip()
            self.clipboard.setText(post_nodesremoved)  # prep modified clipboard data
            nuke.nodePaste('%clipboard%')
            

    def create_postage(self, x, y):
        files = []
        for name in self.read_names:
            source_node = nuke.toNode(name)
            postage = nuke.nodes.PostageStamp(xpos=x, ypos=y)
            postage["hide_input"].setValue(1)
            postage["postage_stamp"].setValue(1)
            postage.setInput(0, source_node)
            #increment x pos value 150 to add gap between nodes
            x += 150

        for name in self.pos_names:
            pn = nuke.toNode(name)
            source_name = pn.input(0).name()
            source_node = nuke.toNode(source_name)
            postage = nuke.nodes.PostageStamp(xpos=x, ypos=y)
            postage["hide_input"].setValue(1)
            postage["postage_stamp"].setValue(1)
            postage.setInput(0, source_node)
            #increment x pos value 150 to add gap between nodes
            x += 150

    def get_pos(self):
        temp_node = nuke.createNode("Dot", inpanel=False)
        x = temp_node.xpos()
        y = temp_node.ypos()
        nuke.delete(temp_node)
        return x, y

    def check_path(self):
        read_count = 0
        for f in range(len(self.read_data)):
            rn = re.findall(r'name (.+)', self.read_data[f])
            rf = re.findall(r'file (.+)', self.read_data[f])
            rns = rn[0].strip('"')
            rfs = rf[0].strip('"')
            sr = nuke.toNode(rns)
            if sr != None:
                read_count += 1
        if len(self.read_data) == read_count:
            return True
        else:
            return False
            

'''
#Add to Menu.py
nuke.menu('Nuke').addCommand('Edit/Paste Hijack', 'import Hijack_Paste;Hijack_Paste.HijackPaste().hijackpaste()', 'ctrl+v')
'''
