import maya.cmds as mc
import math

import random

import maya.api.OpenMaya as om
from RigLibrary.base import control
from Utils import ParentOffsetMatrixTransfer


# CHECKING THE MOTION PATH CURVE

class MotionPathFiller:
    objects = []

    def build(self,
              motionPathCurve="",
              spacingType="",
              spacingValue=1,
              doesPreserveRotation=True,
              randomScale=False,
              randomRotate=False,
              motionPathObjects=[],
              maxScaleRandom = 1):

        # Looking for the motionPathCurve

        objects = []

        spacingCap = 100
        print(motionPathCurve)

        # finding the exact spacing for U values
        position = 0

        spawnRate = (1 / spacingCap) * spacingValue

        # WIP PASSAGE :: We do a duplicate for now
        while position <= 1:
            i = 0

            index = random.randint(0, len(motionPathObjects) - 1)
            print(index)
            object = mc.duplicate(motionPathObjects[index], n=motionPathObjects[index] + "%i" % (i + 1))

            objects.append(object)

            mpName = mc.pathAnimation(object, name=f'motionPathConstraint{i}', follow=True, followAxis='x',
                                        upAxis='y', worldUpType='vector', worldUpVector=(0, 1, 0), fractionMode=True,
                                        curve=motionPathCurve)

            if doesPreserveRotation == False:
                mc.disconnectAttr(mpName + ".uValue", object[0] + ".rotate")

                # breaking  connections of objects

            print(mpName)
            # mc.pathAnimation('motionPathConstraint', edit=True, object=motionPathObjects[index],
            #                   motionPath=mpName)

            uValueNode = mpName + "_uValue"
            mc.disconnectAttr(uValueNode + ".output", mpName + ".uValue")
            mc.setAttr(mpName + '.uValue', position)

            i += 1
            if spacingType == "NORMAL":
                position += spawnRate
            elif spacingType == "RANDOM":
                position += random.uniform(1 / spacingCap, 1 / spacingCap * 10)

        if randomScale == True:
            for obj in objects:
                randomScaleValue = random.uniform(1, maxScaleRandom)
                for axis in ["X","Y","Z"]:
                    mc.setAttr(obj[0] + ".scale"+axis, randomScaleValue)  # adding user control

        if randomRotate == True:
            for obj in objects:
                randomAxis = {1: "X", 2: "Y", 3: "Z"}
                mc.setAttr(obj[0] + ".rotate" + randomAxis[random.randint(1, 3)], random.randint(0, 360))

        return objects

    def MotionPathConstraint(self, objects="", curve="", equidistantSpacing=1):

        position = 0

        for object in objects:
            mpName = mc.pathAnimation(object, name=f'motionPathConstraint_{object}', follow=True, followAxis='x',
                                      upAxis='y', worldUpType='vector', worldUpVector=(0, 1, 0), fractionMode=True,
                                      curve=curve)


            uValueNode = mpName + "_uValue"
            mc.disconnectAttr(uValueNode + ".output", mpName + ".uValue")
            mc.setAttr(mpName + '.uValue', position)

            position += equidistantSpacing

    def Translate(self, canTranslate=True, speed=1, objects=None, driverAttribute ="", locator_name ="") :

        motion_paths = []

        print(f"testing if translation is working correctly {objects}")
        for obj in objects:
            print(obj)
            connections = mc.listConnections(obj,type='motionPath') or []  # Get motion path connections for each selected object
            motion_paths.extend(connections)

        for constraint in motion_paths:
            print(constraint)
            originalUValue = mc.getAttr(constraint + "." + "uValue")

            constraintExpression = f"""

            float $uValueZero;
            $uValueZero = {originalUValue};

            if ($uValueZero + {locator_name}.{driverAttribute} > 1) {{
            {constraint}.uValue = $uValueZero + {locator_name}.{driverAttribute} - 1;
            }}
            else {{
            {constraint}.uValue = $uValueZero + {locator_name}.{driverAttribute};
            }}
            """

            sinNodeExpression = mc.expression(s=constraintExpression, o=constraint)
        print(motion_paths)


"""
import maya.cmds as mc 

import maya.cmds as cmds

# Replace 'your_locator' with the name of your locator
locator_name = 'tread_center_aim_r'

# List all connections from the locator
connections = cmds.listConnections(locator_name, source=False, destination=True)
print(connections)

# Filter out the motion path constraints
motion_path_constraints = [conn for conn in connections if 'motionPath' in cmds.nodeType(conn)]

# Print the names of the motion path constraints
for constraint in motion_path_constraints:
    print("Motion Path Constraint:", constraint)
    
    
    
    import maya.cmds as mc 

import maya.cmds as cmds

drivenAttribute = "uValue"
driverAttribute = "TreadCycle"


motionPaths = []

locator_name = 'tread_center_aim_r'

connections = cmds.listConnections(locator_name, source=False, destination=True)

motion_path_constraints = [conn for conn in connections if 'motionPath' in cmds.nodeType(conn)]

for constraint in motion_path_constraints:
    motionPaths.append(constraint)
    
    originalUValue = mc.getAttr(constraint + "." +"uValue")
    
    import maya.cmds as mc 

import maya.cmds as cmds


"""

# FILLING MOTION PATH WITH OBJECTS

# OR GETTING OBJECTS IN MOTION PATH

# ======================================
# GETTING APPROACH : DEFINING SPEED USING U VALUE IN MOTION PATH
# NORMALISING SPEED TO ADAPT IT TO U ( since U is a % )
# CREATING EXPRESSION
#


# ======================================
# CHECKING MOTION PATH
# FILLING IT WITH OBJECTS DEPENDING OF SPACING ATTRIBUTE
# ADDING SPEED TRANSLATION
# RANDOM SCALE
# RANDOM SPACING
# HIDING CURVE
