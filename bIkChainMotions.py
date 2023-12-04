import math

import maya.api.OpenMaya as om
import maya.cmds as mc


from RigLibrary.base import control

from Utils import ParentOffsetMatrixTransfer


def Spread(pivotChain = 0, ikChains = [], spreadFactor = 1, spreadDirection = "", spreadPhases = [], spreadroot = {} ):
    pass

    ikChainsNumber = len(ikChains)
    singleIkChainNum = len(ikChains[0])

    leftChains = ikChains[:pivotChain]
    rightChains = ikChains[pivotChain+1:]

    #writing expressions for left side and right side

    #right do right rotation

    #WIP adding clamping
    #WIP adding spreadConvergence divergence
    #WIP adding speed
    #WIP adding initial offset variable that is already set in

    mc.addAttr(spreadroot, longName="spreadFactor", attributeType='double', defaultValue=1.0, keyable=True)

    for j in range (len(leftChains)):
        mainRotatorJoint = leftChains[j][0]
        spreadExpression = f"""
                            {leftChains[j][0]}.rotate{spreadDirection} =  ({spreadroot}.spreadFactor * {spreadPhases[j]});             
                                """
        spreadNodeExpression = mc.expression(s=spreadExpression, o=leftChains[j][0])

    for j in range (len(rightChains)):
        mainRotatorJoint = rightChains[j][0]
        spreadExpression = f"""
                            {rightChains[j][0]}.rotate{spreadDirection} = (-{spreadroot}.spreadFactor * {spreadPhases[j]});             
                                """
        spreadNodeExpression = mc.expression(s=spreadExpression, o=rightChains[j][0])



    """
    sinExpression = 

                    float $frame;
                    $frame = `currentTime -q`;
                    float $sinWaveValueZ = {ctrl.C}.amplitudeZ * sin( ($frame * {ctrl.C}.frequencyZ)  + {i} *  {ctrl.C}.phaseOffsetZ + {ctrl.C}.offsetZ);
                    float $sinWaveValueX = {ctrl.C}.amplitudeX * sin( ($frame * {ctrl.C}.frequencyX)  + {i} *  {ctrl.C}.phaseOffsetX + {ctrl.C}.offsetX);
                    float $sinWaveValueY = {ctrl.C}.amplitudeY * sin( ($frame * {ctrl.C}.frequencyY)  + {i} *  {ctrl.C}.phaseOffsetY + {ctrl.C}.offsetY);
                    {ctrls[i].C}.translateZ = $sinWaveValueZ;
                    {ctrls[i].C}.translateY = $sinWaveValueY;
                    {ctrls[i].C}.translateX = $sinWaveValueX;

                                    
    """

def  Curl():
    pass


def SinMotion():
    pass



