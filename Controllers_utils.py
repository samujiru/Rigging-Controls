"""
This util module provides functions to generate common rigging shapes 
with customizable scales and automatic organizational grouping options.
"""

import maya.cmds as cmds

def create_circle(name="ctrl_circle", radius=1.0):
    # This line generates the circle and returns the transform name
    cmds.select(cl=True)
    obj = cmds.circle(name=name, r=radius, ch=False)[0]
    return obj

def create_cube(name="ctrl_cube", scale=1.0):
    #This line ensures selections are cleared
    cmds.select(cl=True)
    s = scale
    pts = [(-s,s,s), (s,s,s), (s,-s,s), (-s,-s,s), (-s,s,s), (-s,s,-s), (s,s,-s), 
           (s,-s,-s), (-s,-s,-s), (-s,s,-s), (-s,-s,-s), (-s,-s,s), (s,-s,s), 
           (s,-s,-s), (s,s,-s), (s,s,s)]
    
    # This line creates the cube shape by drawing a linear curve
    obj = cmds.curve(name=name, d=1, p=pts)
    return obj

def create_sphere(name="ctrl_sphere", radius=1.0):
    #This line ensures selections are cleared
    cmds.select(cl=True)
# These lines create three circles on different axes to form a sphere
    c1 = cmds.circle(nr=(1, 0, 0), r=radius, ch=False)[0]
    c2 = cmds.circle(nr=(0, 1, 0), r=radius, ch=False)[0]
    c3 = cmds.circle(nr=(0, 0, 1), r=radius, ch=False)[0]

    #This line creates a master transform node
    master_ctrl = cmds.group(em=True, name=name)
    
    # This line groups the three circles into one organizational node
    for circle in [c1, c2, c3]:
        shapes = cmds.listRelatives(circle, shapes=True)
        if shapes:
            cmds.parent(shapes,master_ctrl, shape=True, relative=True)
        cmds.delete(circle)

    cmds.select(cl=True)
    return master_ctrl

def create_pyramid(name="ctrl_pyramid", scale=0.5):
    #This line ensures selections are cleared
    cmds.select(cl=True)
    s = scale
    # These points draw the square base, then trace up to the apex point at the top
    pts = [(-s,0,-s), (s,0,-s), (s,0,s), (-s,0,s), (-s,0,-s), 
           (0,s*1.5,0), (s,0,-s), (s,0,s), (0,s*1.5,0), (-s,0,s)]
    
    # This line creates the pyramid shape using a linear NURBS curve
    obj = cmds.curve(name=name, d=1, p=pts)
    return obj

def create_gear(name="ctrl_gear", radius=1.0):
    #This line ensures selections are cleared
    cmds.select(cl=True)
    # This line creates a high-span circle to act as the gear base
    obj = cmds.circle(name=name, degree=1, sections=16, r=radius, ch=False)[0]
    return obj
