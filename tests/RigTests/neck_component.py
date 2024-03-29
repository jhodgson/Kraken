from kraken.core.maths.vec import Vec3
from kraken.core.maths.xfo import Xfo

from kraken.core.objects.attributes.bool_attribute import BoolAttribute
from kraken.core.objects.attributes.float_attribute import FloatAttribute
from kraken.core.objects.constraints.pose_constraint import PoseConstraint
from kraken.core.objects.components.base_component import BaseComponent
from kraken.core.objects.locator import Locator
from kraken.core.objects.joint import Joint
from kraken.core.objects.srtBuffer import SrtBuffer
from kraken.core.objects.controls.pin_control  import PinControl

from kraken.core.objects.operators.splice_operator import SpliceOperator


class NeckComponent(BaseComponent):
    """Neck Component"""

    def __init__(self, name, parent=None, location='M'):
        super(NeckComponent, self).__init__(name, parent, location)

        # Setup component attributes
        defaultAttrGroup = self.getAttributeGroupByIndex(0)
        defaultAttrGroup.addAttribute(BoolAttribute("toggleDebugging", True))

        # Default values
        neckPosition = Vec3(0.0, 16.5572, -0.6915)
        neckUpV = Vec3()
        neckUpV.copy(neckPosition)
        neckUpV = neckUpV.add(Vec3(0.0, 0.0, -1.0)).unit()
        neckEndPosition = Vec3(0.0, 17.4756, -0.421)

        # Calculate Clavicle Xfo
        rootToEnd = neckEndPosition.subtract(neckPosition).unit()
        rootToUpV = neckUpV.subtract(neckPosition).unit()
        bone1ZAxis = rootToUpV.cross(rootToEnd).unit()
        bone1Normal = bone1ZAxis.cross(rootToEnd).unit()
        neckXfo = Xfo()
        neckXfo.setFromVectors(rootToEnd, bone1Normal, bone1ZAxis, neckPosition)

        # Add Guide Controls
        neckCtrlSrtBuffer = SrtBuffer('neck', parent=self)
        neckCtrlSrtBuffer.xfo.copy(neckXfo)

        neckCtrl = PinControl('neck', parent=neckCtrlSrtBuffer)
        neckCtrl.scalePoints(Vec3(1.25, 1.25, 1.25))
        neckCtrl.translatePoints(Vec3(0, 0, -0.5))
        neckCtrl.rotatePoints(90, 0, 90)
        neckCtrl.xfo.copy(neckXfo)
        neckCtrl.setColor("orange")


        # ==========
        # Deformers
        # ==========
        container = self.getParent().getParent()
        deformersLayer = container.getChildByName('deformers')

        neckDef = Joint('neck', parent=deformersLayer)
        neckDef.setComponent(self)


        # =====================
        # Create Component I/O
        # =====================
        # Setup Component Xfo I/O's
        neckEndInput = Locator('neckBase')
        neckEndInput.xfo.copy(neckXfo)
        neckEndOutput = Locator('neckEnd')
        neckEndOutput.xfo.copy(neckXfo)
        neckOutput = Locator('neck')
        neckOutput.xfo.copy(neckXfo)

        # Setup componnent Attribute I/O's
        debugInputAttr = BoolAttribute('debug', True)
        rightSideInputAttr = BoolAttribute('rightSide', location is 'R')


        # ==============
        # Constrain I/O
        # ==============
        # Constraint inputs
        clavicleInputConstraint = PoseConstraint('_'.join([neckCtrl.getName(), 'To', neckEndInput.getName()]))
        clavicleInputConstraint.setMaintainOffset(True)
        clavicleInputConstraint.addConstrainer(neckEndInput)
        neckCtrlSrtBuffer.addConstraint(clavicleInputConstraint)

        # Constraint outputs
        neckEndConstraint = PoseConstraint('_'.join([neckEndOutput.getName(), 'To', neckCtrl.getName()]))
        neckEndConstraint.addConstrainer(neckCtrl)
        neckEndOutput.addConstraint(neckEndConstraint)


        # ==================
        # Add Component I/O
        # ==================
        # Add Xfo I/O's
        self.addInput(neckEndInput)
        self.addOutput(neckEndOutput)
        self.addOutput(neckOutput)

        # Add Attribute I/O's
        self.addInput(debugInputAttr)
        self.addInput(rightSideInputAttr)


        # ===============
        # Add Splice Ops
        # ===============
        # Add Deformer Splice Op
        # spliceOp = SpliceOperator("neckDeformerSpliceOp", "PoseConstraintSolver", "KrakenPoseConstraintSolver")
        # self.addOperator(spliceOp)

        # # Add Att Inputs
        # spliceOp.setInput("debug", debugInputAttr)
        # spliceOp.setInput("rightSide", rightSideInputAttr)

        # # Add Xfo Inputstrl)
        # spliceOp.setInput("constrainer", neckEndOutput)

        # # Add Xfo Outputs
        # spliceOp.setOutput("constrainee", neckDef)


    def buildRig(self, parent):
        pass


if __name__ == "__main__":
    neck = NeckComponent("myNeck", location='M')
    print neck.getNumChildren()