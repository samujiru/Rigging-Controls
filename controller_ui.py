"""
This module provides an interface for the Rigging Controller tool.  
It allows users to select a shape, name it, choose its size without affecting the transformations of the
curve and generate it.
"""

import sys
import os

# Safe path insertion AFTER sys is imported
sys.path.insert(0, r"C:\Users\sgj01\OneDrive\Documents\maya\projects\default\scripts")

# Dynamic UI framework selection to support Maya 2025/2026 (PySide6) and older versions (PySide2)
try:
    from PySide6 import QtWidgets, QtCore, QtGui
except ImportError:
    from PySide2 import QtWidgets, QtCore, QtGui

# This line brings in the main rigging script
import Main
import importlib
importlib.reload(Main)

# This line is in charge of the dialogue for the UI popup
class RiggingControllerUI(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(RiggingControllerUI, self).__init__(parent)
        
        self.setWindowTitle("Rig Controller Builder")
        self.setMinimumWidth(300)
        
        # This line ensures the UI stays on top of the other Maya elements
        self.setWindowFlags(QtCore.Qt.Window)
        
        self.create_widgets()
        self.create_layout()
        self.create_connections()
        
    # This line initializes all of the UI elements  
    def create_widgets(self):
        # This line is for the UI dropdown menu
        self.shape_label = QtWidgets.QLabel("Controller Shape:")
        self.shape_combo = QtWidgets.QComboBox()
        self.shape_combo.addItems(["circle", "cube", "sphere", "pyramid", "gear"])
        
        # This line allows you to name your elements
        self.name_label = QtWidgets.QLabel("Base Name:")
        self.name_input = QtWidgets.QLineEdit()
        self.name_input.setPlaceholderText("e.g., hand, foot, spine")
        
        # This line allows you to control the size of your controller
        self.size_label = QtWidgets.QLabel("Size/Scale:")
        self.size_spin = QtWidgets.QDoubleSpinBox()
        self.size_spin.setRange(0.1, 100.0)
        self.size_spin.setValue(1.0)
        self.size_spin.setSingleStep(0.5)
        
        # This line applies any changes you've made and creates the control
        self.build_btn = QtWidgets.QPushButton("Build Controller")
        # This line darkens the button to match with Maya's UI
        self.build_btn.setStyleSheet("background-color: #557a55; font-weight: bold; height: 30px;")

    # This line fits the widgets using a form and main layout  
    def create_layout(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        
        # This line has the form layout for parameter inputs
        form_layout = QtWidgets.QFormLayout()
        form_layout.setSpacing(10)
        form_layout.addRow(self.shape_label, self.shape_combo)
        form_layout.addRow(self.name_label, self.name_input)
        form_layout.addRow(self.size_label, self.size_spin)
        
        # This line adds to main layout
        main_layout.addLayout(form_layout)
        
        # This line does some minor UI tweaks like adding a visual separator line
        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        main_layout.addWidget(line)
        
        # This line creates the build button
        main_layout.addWidget(self.build_btn)

    # This line connects the UI signals to the function of the python methods  
    def create_connections(self):
        self.build_btn.clicked.connect(self.on_build_clicked)

    # This line receives the data from the UI, and runs them through the Main script  
    def on_build_clicked(self):
        shape = self.shape_combo.currentText()
        name = self.name_input.text().strip()
        size = self.size_spin.value()
        
        # This line applies a default name if left empty
        if not name:
            name = f"default_{shape}"
            
        try:
            # This line sets the position of the curve at the origin
            result = Main.build_controller(shape=shape, name=name, pos=(0, 0, 0), size=size)
            # This line prints a success message
            QtWidgets.QMessageBox.information(self, "Success", f"Created hierarchy: {result}")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to build controller.\nError: {str(e)}")


# This block is responsible for keeping the UI window safely in Maya
# It uses Maya's main window as the parent so this UI doesn't vanish behind it
def show_ui():
    import maya.mel as mel
    
    try:
        from maya.api import OpenMayaUI as omui
        maya_main_window_ptr = omui.MQtUtil.mainWindow()
        
        # Dynamically import the correct shiboken version based on available PySide
        try:
            import shiboken6 as shiboken
        except ImportError:
            import shiboken
            
        parent_window = shiboken.wrapInstance(int(maya_main_window_ptr), QtWidgets.QWidget)
    except Exception as e:
        print(f"# Warning: Could not parent to Maya main window: {e}")
        parent_window = None

    # Global variable to prevents multiple copies of the same window from popping up
    global global_rig_ui
    
    try:
        global_rig_ui.close()
        global_rig_ui.deleteLater()
    except NameError:
        pass

    # This line prevents Maya from forgetting your custom controls by tying it to a global variable
    global_rig_ui = RiggingControllerUI(parent=parent_window)
    # This line gives the window a size depending on the aspect ratio and size of your monitor
    global_rig_ui.show()
