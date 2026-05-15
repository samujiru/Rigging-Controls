"""
This is the main entry point for the Rigging Controller tool. It also provides a self-test to verify all controller types in the viewport.
"""

import sys
import os
import maya.cmds as cmds

# This block ensures Maya can find the controller_utils module in this folder
path = os.path.dirname(__file__)
if path not in sys.path:
    sys.path.append(path)

import controller_utils
import importlib
importlib.reload(controller_utils)

def build_controller(shape="circle", name="new_ctrl", use_group=True, pos=(0,0,0)):
    node = None
    
    # These lines determine which utility function to call based on the shape argument
    if shape == "circle":
        node = controller_utils.create_circle(name=name, position=pos)
    elif shape == "cube":
        node = controller_utils.create_cube(name=name, position=pos)
    elif shape == "sphere":
        node = controller_utils.create_sphere(name=name, position=pos)
    elif shape == "ball":
        node = controller_utils.create_ball(name=name, position=pos)
    elif shape == "gear":
        node = controller_utils.create_gear(name=name, position=pos)
        
    # This line creates an offset group for the controller if requested
    if use_group and node:
        node = cmds.group(node, name=f"{node}_OFFSET")
        
    return node

if __name__ == "__main__":
    # This line clears the current Maya scene for a fresh test
    cmds.file(new=True, force=True)
    
    # This list defines the types of controllers to generate for the test
    test_list = ["circle", "cube", "sphere", "ball", "gear"]
    
    # This loop iterates through the list to build each controller in the viewport
    for i, shape_type in enumerate(test_list):
        build_controller(shape=shape_type, name=f"test_{shape_type}", pos=(i*4, 0, 0))
    
    print("Self-test complete: 5 controller types generated.")
