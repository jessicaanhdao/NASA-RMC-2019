import wpilib
from networktables import NetworkTables


class BumpSwitch:
    left_bump = wpilib.DigitalInput
    right_bump = wpilib.DigitalInput
    
    def __init__(self):
        self.enabled = False
        self.sd = NetworkTables.getTable('/SmartDashboard')
        #self.goalFound = self.sd.getAutoUpdateValue('ObjectFound',False)
    def isPressing(self):
        pass
    def update(self):
        self.sd.putBoolean("LeftBump",self.left_bump.get())
        #print("left: ",self.left_bump.get())
        self.sd.putBoolean("RightBump",self.right_bump.get())
    def execute(self):
        self.update()