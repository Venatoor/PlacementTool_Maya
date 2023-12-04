from PySide2 import QtCore
from PySide2 import QtUiTools
from PySide2 import QtWidgets
from PySide2 import QtGui
from shiboken2 import wrapInstance

from Techniques import bMotionPathTranslation

import maya.cmds as mc
import maya.OpenMayaUI as omui


def maya_main_window():
    """
    Return the Maya main window widget as a Python object
    """
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


class MotionPathDialog(QtWidgets.QDialog):

    def __init__(self, parent = maya_main_window()):
        super(MotionPathDialog, self).__init__(parent)

        self.setWindowTitle("Placement Tool")
        self.setMinimumWidth(425)
        self.setMinimumHeight(415)

        self.motionPathLogic = bMotionPathTranslation

        self.selectionType = "Selection"
        self.spacingType = "NORMAL"
        self.randomScale = False
        self.spacingValue = 0
        self.preserveNormal = False
        self.randomRotation = False

        self.currentSelection = []


        self.init_ui()
        self.create_layout()
        self.create_connections()


    def init_ui(self):
        loader = QtUiTools.QUiLoader()
        self.ui = loader.load("D:\Animations\Qt\PathTool.ui", parentWidget=None)


    def create_layout(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.ui)

    def create_connections(self):
        #self.ui.selectionList.itemDoubleClicked.connect(self.OnSelectTab)
        #self.ui.allowTimerChB.stateChanged.connect(self.OnAllowTimerToggled)
        #self.ui.timedSaveValueLE.editingFinished.connect(self.OnTimedSaveValueFinishEditing)
        #self.ui.timedSaveSuffixLE.editingFinished.connect(self.OnTimedSaveSuffixesFinishEditing)
        #self.ui.querySavesPB.clicked.connect(self.OnQuerySavesClicked)

        self.ui.curveSelectionTypeCB.activated.connect(self.on_curve_type_changed)
        self.ui.spacingTypeCB.activated.connect(self.on_spacing_type_changed)
        self.ui.normalChB.stateChanged.connect(self.on_preserve_normal_directions_toggled)
        self.ui.randomRotChB.stateChanged.connect(self.on_random_rotation_toggled)
        self.ui.randomScaleChB.stateChanged.connect(self.on_random_scale_toggled)

        self.ui.addObjectPB.clicked.connect(self.on_add_object)
        self.ui.deleteObjectPB.clicked.connect(self.on_delete_object)
        self.ui.clearObjectPB.clicked.connect(self.on_clear)

        self.ui.addPB.clicked.connect(self.on_apply)

    def on_random_scale_toggled(self):
        if self.ui.randomScaleChB.isChecked():
            self.randomScale = True
        else:
            self.randomScale = False

    def on_preserve_normal_directions_toggled(self):
        if self.ui.normalChB.isChecked():
            self.preserveNormal = True
        else:
            self.preserveNormal = False

    def on_random_rotation_toggled(self):
        if self.ui.randomRotChB.isChecked():
            self.randomRotation = True
        else:
            self.randomRotation = False

    def on_curve_type_changed(self):
        self.selectionType = self.ui.curveSelectionTypeCB.currentText()

    def on_spacing_type_changed(self):
        self.spacingType = self.ui.spacingTypeCB.currentText()

    def on_apply(self):
        curves = mc.ls(sl = 1)
        print(f"THE SELECTED CURVES ARE : {curves}")
        for curve in curves:
                #quick verification of null values
                self.spacingValue = float(self.ui.spacingValueLE.text())
                if self.spacingValue != 0 and len(self.currentSelection) != 0 :
                    print("Verifying if it works")
                    motionPath = bMotionPathTranslation.MotionPathFiller
                    concernedObjects = motionPath.build(self,motionPathCurve= curve,
                                                                  spacingType=  self.spacingType,
                                                                  spacingValue= self.spacingValue,
                                                                  doesPreserveRotation= self.preserveNormal,
                                                                  randomScale= self.randomScale,
                                                                  randomRotate= self.randomRotation,
                                                                  motionPathObjects= self.currentSelection,
                                                                  maxScaleRandom= 1.5
                                                                  )
                    if len(self.ui.translationCtrlLE.text()) != 0 and len(self.ui.translationAttLE.text()) != 0 :
                        if mc.objExists(self.ui.translationCtrlLE.text()):
                            if mc.attributeQuery(self.ui.translationAttLE.text(),
                                                 node=self.ui.translationCtrlLE.text(),
                                                 exists=True):
                                bMotionPathTranslation.MotionPathFiller.Translate(self,
                                                                                  canTranslate=True,
                                                                                  speed=1,
                                                                                  objects=concernedObjects,
                                                                                    driverAttribute =self.ui.translationAttLE.text(),
                                                                                  locator_name =self.ui.translationCtrlLE.text())
                            else:
                                print("The Attribute was not found on the driver")
                        else:
                            print("The Driver for the Motion Path Translation does not exist")
                    else :
                        print("Enter a translation control and a translation control attribute ")

                else:
                    print("Enter a spacing value and have a current selection")



    def isCurve(self, objName):
        objectType = mc.objectType(objName)
        print(objectType)
        return objectType in ["transform"]

    #selection

    def on_add_object(self):
        objects = mc.ls(sl=1)
        for object in objects:
            if object in self.currentSelection:
                return False
            else:
                for obj in objects:
                    # Assuming self.ui.selectionObjectsLW is your QListWidget
                    self.ui.selectionObjectsLW.addItem(obj)
                    self.currentSelection.append(obj)
                    print(objects)
                    #TODO VERIFY IS OBJECTS ALREADY EXIST


    def on_delete_object(self):
        objects = mc.ls(sl=1)
        for obj in objects:
            # Assuming self.ui.selectionObjectsLW is your QListWidget
            self.ui.selectionObjectsLW.removeItem(obj)
            self.currentSelection.remove(obj)
            print(objects)

    def on_clear(self):
        self.currentSelection.clear()


if __name__ == "__main__":

    motionPathUI = MotionPathDialog()
    motionPathUI.show()


