"""

Simple Blender python script to verify the 2014 vector calculation works as intended for the 2010 Maya project. 
I cannot justify getting a Maya license to run the original script for the cost. 

"""

import bpy;
import random;
import math as m;

# Draw one object at center
location = (0, 0, 0)

bpy.ops.mesh.primitive_cube_add(
    size=2,
    enter_editmode=False,
    align='WORLD',
    location=location,
    scale=(1, 1, 1)) 

# Vector rotation
aRotationX = 30
aRotationZ = 60


# Calculate Direction
"""
Blender did not have a working pi utility
"""
myPi = 3.141592653589793
radiansX = myPi * aRotationX / 180
radiansZ = myPi * aRotationZ / 180

vectorLength = 5

# Calculate vector endpoint x,y,z
x1 = vectorLength * m.sin(radiansZ)
y1 = vectorLength * (m.cos(radiansZ) * m.cos(radiansX))
z1 = vectorLength * (m.cos(radiansZ) * m.sin(radiansX))

# Draw second object at end of vector 
location1 = (x1, y1, z1)
  
bpy.ops.mesh.primitive_cube_add(
    size=2,
    enter_editmode=False,
    align='WORLD',
    location=location1,
    scale=(1, 1, 1))    
    