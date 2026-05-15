"""
This util module provides functions to generate common rigging shapes 
with customizable scales and automatic organizational grouping options.
"""

import maya.cmds as cmds

def create_circle(name="ctrl_circle", radius=1.0, position=(0, 0, 0)):
    #This line generates the NURBS circle and captures the transform name
    obj = cmds.circle(name=name, r=radius, ch=False)[0]
    #This line moves the controller to the specified position
    cmds.move(position[0], position[1], position[2], obj)
    return obj

def create_cube(name="ctrl_cube", scale=1.0, position=(0, 0, 0)):
    s = scale
    pts = [(-s,s,s), (s,s,s), (s,-s,s), (-s,-s,s), (-s,s,s), (-s,s,-s), (s,s,-s), 
           (s,-s,-s), (-s,-s,-s), (-s,s,-s), (-s,-s,-s), (-s,-s,s), (s,-s,s), 
           (s,-s,-s), (s,s,-s), (s,s,s)]
    
#This line creates the cube shape by drawing a degree 1 (linear) curve
    obj = cmds.curve(name=name, d=1, p=pts)
    #This line moves the cube to the specified position
    cmds.move(position[0], position[1], position[2], obj)
    return obj

def create_sphere(name="ctrl_sphere", radius=1.0, position=(0, 0, 0)):
    #These lines create three circles on different axes to form a sphere
    c1 = cmds.circle(nr=(1, 0, 0), r=radius, ch=False)[0]
    c2 = cmds.circle(nr=(0, 1, 0), r=radius, ch=False)[0]
    c3 = cmds.circle(nr=(0, 0, 1), r=radius, ch=False)[0]
    
    #This line groups the three circles into one organizational node
    obj = cmds.group(c1, c2, c3, name=name)
    #This line moves the entire sphere group to the specified position
    cmds.move(position[0], position[1], position[2], obj)
    return obj

def create_ball(name="ctrl_ball", scale=0.5, position=(0, 0, 0)):
    s = scale
    pts = [(0,s,0), (s,0,0), (0,0,s), (0,s,0), (-s,0,0), (0,0,s), (0,-s,0), (s,0,0)]
    
    #This line creates the diamond shape using a linear NURBS curve
    obj = cmds.curve(name=name, d=1, p=pts)
    #This line moves the controller to the specified position
    cmds.move(position[0], position[1], position[2], obj)
    return obj

def create_gear(name="ctrl_gear", radius=1.0, position=(0, 0, 0)):
    #This line creates a high-span circle to act as the gear base
    obj = cmds.circle(name=name, degree=1, sections=16, r=radius, ch=False)[0]
    #This line moves the gear to the specified position
    cmds.move(position[0], position[1], position[2], obj)
    return obj
