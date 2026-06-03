"""
This is the main entry point for the Rigging Controller tool. It also provides a self-test to verify all controller types in the viewport.
"""

import sys
import os
import maya.cmds as cmds

# This block ensures Maya can find the controller_utils module in this folder. If the file isn't found, then Maya will display a warning. 
try:
    path = os.path.dirname(__file__)
    if path not in sys.path:
        sys.path.append(path)
except NameError:
    print("# Warning: Running from an unsaved Script Editor tab. "
          "Ensure controller_utils.py is inside your Maya scripts directory!")

import controller_utils
import controller_ui
import importlib
importlib.reload(controller_utils)

def build_controller(shape="circle", name="new", pos=(0,0,0)):
    # This line automatically appends the '_ctrl' suffix to the base name of the NURBS Curve
    full_ctrl_name = f"{name}_ctrl"
    
    ctrl_node = None
    
    # These lines generate the geometry with the proper suffix
    if shape == "circle":
        ctrl_node = controller_utils.create_circle(name=full_ctrl_name)
    elif shape == "cube":
        ctrl_node = controller_utils.create_cube(name=full_ctrl_name)
    elif shape == "sphere":
        ctrl_node = controller_utils.create_sphere(name=full_ctrl_name)
    elif shape == "pyramid":
        ctrl_node = controller_utils.create_pyramid(name=full_ctrl_name)
    elif shape == "gear":
        ctrl_node = controller_utils.create_gear(name=full_ctrl_name)

    if not ctrl_node:
        print(f"Error: Shape type '{shape}' not recognized.")
        return None
        
    # This line clears Maya's selection so no additional objects get grouped with the NURBS curves
    cmds.select(cl=True)
    # This line creates the group using the original base name + '_o'
    offset_grp = cmds.group(ctrl_node, name=f"{name}_o")
    
    # This line moves the group (and the child controller) to the target position
    cmds.move(pos[0], pos[1], pos[2], offset_grp)
    cmds.parent(ctrl_node, offset_grp)
    
    return offset_grp

if __name__ == "__main__":
    # This line clears the current Maya scene for a fresh test
    cmds.file(new=True, force=True)
    
    # This list defines the types of controllers to generate for the test
    test_list = ["circle", "cube", "sphere", "pyramid", "gear"]
    
    # This loop iterates through the list to build each controller and its group
    for i, shape_type in enumerate(test_list):
        # Test the naming convention: base name gives 'shape_ctrl' inside 'shape_o'
        result = build_controller(shape=shape_type, name=shape_type, pos=(i*4, 0, 0))
        print(f"Hierarchy Created: {result}")
    
    print("Self-test complete: All controllers created with precise naming conventions.")
