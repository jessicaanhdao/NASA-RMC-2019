import ctre, wpilib
from networktables import NetworkTables


class CameraServo:
    

    # speed is tunable via NetworkTables
  #  shoot_speed = tunable(1.0)

    def __init__(self):
        self.enabled = False
        self.sd = NetworkTables.getTable('/SmartDashboard')

        #servo
        self.leftServo = wpilib.Servo(0)
        self.rightServo = wpilib.Servo(1)
        self.leftServo.set(0)
        
        self.rightServo.set(0)
        #camera stuff
        self.leftCam = self.sd.getAutoUpdateValue('LeftCam',False)
        self.rightCam = self.sd.getAutoUpdateValue('RightCam',False)
        self.goalFound = self.sd.getAutoUpdateValue('GoalFound',False)

    def enable(self):
        '''Causes the shooter motor to spin'''
        self.enabled = True
    def reset(self):
        self.leftServo.setAngle(0)
        self.rightServo.setAngle(0)
       
    def findGoal(self):
        #while (not self.leftCam and not self.rightCam):
        i=0
        
        while (i < 6):
            #langle =0
            self.leftServo.setAngle(self.leftServo.getAngle()+30)
            print(self.leftServo.getAngle())
            self.rightServo.setAngle(self.rightServo.getAngle()+30)
            print(self.rightServo.getAngle())
            i=i+1
        '''if (self.leftCam):
            angle = self.leftServo.getAngle()
        elif (self.rightCam):
            angle = self.rightServo.getAngle()
        if (self.goalFound):
            #left cam vs right cam
            self.sd.putNumber('Servo',angle)'''

    def execute(self):
        '''This gets called at the end of the control loop'''
        self.enabled = False
        wpilib.Timer.delay(0.005)