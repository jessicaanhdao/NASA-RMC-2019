import ctre
from networktables import NetworkTables


class Camera:
    
    def __init__(self):
        self.enabled = False
        self.sd = NetworkTables.getTable('/SmartDashboard')
        self.goalFound = self.sd.getAutoUpdateValue('ObjectFound',False)
        self.leftCam = self.sd.getAutoUpdateValue('LeftCam',False)
        self.rightCam = self.sd.getAutoUpdateValue('RightCam',False)
    def enable(self):
        '''Causes the shooter motor to spin'''
        self.enabled = True

    def isGoalFound(self):
        if(self.goalFound.value):
           return True
        return False
    def isFrontFacingUp(self):
        if (self.rightCam):
            return True
        else:
            return False
    
    def execute(self):
        #self.enabled = True
        pass
    