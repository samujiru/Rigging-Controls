"""
This module has PySide6 dialog for Maya 2026. It lets the artist pick a shape,
         name it, set its size, toggle the offset group, and call Main.build_controller() to create it in the scene.
"""

import sys
import os

#This line gives the code a fallback in case the files aren't found
try:
    _scripts_dir = os.path.dirname(os.path.abspath(__file__))
    if _scripts_dir not in sys.path:
        sys.path.insert(0, _scripts_dir)
except NameError:
    _fallback = r"C:\Users\sgj01\OneDrive\Documents\maya\projects\default\scripts"
    if _fallback not in sys.path:
        sys.path.insert(0, _fallback)
    print("# Warning: __file__ not available — using fallback scripts path.")

from PySide6 import QtWidgets, QtCore, QtGui
from shiboken6 import wrapInstance
from maya.api import OpenMayaUI as omui

import Main as Main
import importlib
importlib.reload(Main)

#This line returns maya's main window wrapped as a QWidget
def _get_maya_Main_window():
    try:
        ptr = omui.MQtUtil.MainWindow()
        return wrapInstance(int(ptr), QtWidgets.QWidget)
    except Exception as e:
        print("# Warning: Could not resolve Maya Main window: {}".format(e))
        return None

#This is the rigging controller builder
class RiggingControllerUI(QtWidgets.QDialog):

    WINDOW_TITLE = "Rig Controller Builder"
    OBJECT_NAME  = "RigControllerBuilderUI"

    def __init__(self, parent=None):
        super(RiggingControllerUI, self).__init__(parent)

        self.setWindowTitle(self.WINDOW_TITLE)
        self.setObjectName(self.OBJECT_NAME)
        self.setMinimumWidth(320)

        self.setWindowFlags(QtCore.Qt.WindowType.Window)

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        """Instantiate every UI control."""

        #These lines is the shape dropdown
        self.shape_label = QtWidgets.QLabel("Controller Shape:")
        self.shape_combo = QtWidgets.QComboBox()
        self.shape_combo.addItems(["circle", "cube", "sphere", "pyramid", "gear"])

        #These line is the base name
        self.name_label = QtWidgets.QLabel("Base Name:")
        self.name_input = QtWidgets.QLineEdit()
        self.name_input.setPlaceholderText("e.g. hand, foot, spine")

        #These lines are for zize
        self.size_label = QtWidgets.QLabel("Size:")
        self.size_spin  = QtWidgets.QDoubleSpinBox()
        self.size_spin.setRange(0.01, 1000.0)
        self.size_spin.setValue(1.0)
        self.size_spin.setSingleStep(0.5)
        self.size_spin.setDecimals(2)

        #These lines toggle the offset group
        self.offset_grp_label    = QtWidgets.QLabel("Offset Group:")
        self.offset_grp_checkbox = QtWidgets.QCheckBox("Create offset group (zero-out)")
        self.offset_grp_checkbox.setChecked(True)
        self.offset_grp_checkbox.setToolTip(
            "Creates a '_GRP' node above the controller so its local channels "
            "read zero while the group holds the world-space position."
        )

        #These lines are for the build button
        self.build_btn = QtWidgets.QPushButton("Build Controller")
        self.build_btn.setStyleSheet(
            "QPushButton          { background-color: #557a55; color: #ffffff; "
            "                       font-weight: bold; height: 30px; border-radius: 4px; }"
            "QPushButton:hover    { background-color: #6a9b6a; }"
            "QPushButton:pressed  { background-color: #3f5e3f; }"
        )

         #These lines arrange the widgets
    def create_layout(self):
        Main_layout = QtWidgets.QVBoxLayout(self)
        Main_layout.setSpacing(8)
        Main_layout.setContentsMargins(12, 12, 12, 12)

        form = QtWidgets.QFormLayout()
        form.setSpacing(8)
        form.addRow(self.shape_label,      self.shape_combo)
        form.addRow(self.name_label,       self.name_input)
        form.addRow(self.size_label,       self.size_spin)
        form.addRow(self.offset_grp_label, self.offset_grp_checkbox)

        Main_layout.addLayout(form)

        #These lines are for the visual separator
        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        Main_layout.addWidget(line)

        Main_layout.addWidget(self.build_btn)

    def create_connections(self):
        self.build_btn.clicked.connect(self.on_build_clicked)

         #These lines read the UI values and call buld_controller()
    def on_build_clicked(self):
        shape      = self.shape_combo.currentText()
        name       = self.name_input.text().strip()
        size       = self.size_spin.value()
        offset_grp = self.offset_grp_checkbox.isChecked()

        if not name:
            name = "default_{}".format(shape)

        try:
            result = Main.build_controller(
                shape=shape,
                name=name,
                pos=(0, 0, 0),
                size=size,
                offset_grp=offset_grp
            )
            ctrl_name = "{}_CTRL".format(name)
            print("# Rig Controller Builder: created '{}'.".format(result))
            QtWidgets.QMessageBox.information(
                self,
                "Controller Created",
                "'{}' was added to the scene.".format(ctrl_name)
            )
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self,
                "Build Failed",
                "Could not create the controller.\n\nError:\n{}".format(str(e))
            )


_rig_ui_instance = None


#These lines open the rigging controller bulder as a singleton dialog
def show_ui():
    """
    Open the Rigging Controller Builder as a singleton dialog.

    Safe to call multiple times — the previous window is closed and
    replaced so that hot-reloading the module always gives a fresh instance.
    """
    global _rig_ui_instance

    try:
        _rig_ui_instance.close()
        _rig_ui_instance.deleteLater()
    except Exception:
        pass

    parent = _get_maya_Main_window()
    _rig_ui_instance = RiggingControllerUI(parent=parent)
    _rig_ui_instance.show()
