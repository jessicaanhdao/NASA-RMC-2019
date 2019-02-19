import ctre
from networktables import NetworkTables


class Camera:
    
    def __init__(self):
        self.enabled = False
        self.sd = NetworkTables.getTable('/SmartDashboard')
        self.goalFound = self.sd.getAutoUpdateValue('ObjectFound',False)
    def enable(self):
        '''Causes the shooter motor to spin'''
        self.enabled = True

    def isGoalFound(self):
        if(self.goalFound.value):
           return True
        return False
    def execute(self):
        self.enabled = True