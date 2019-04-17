import ctre, wpilib
from networktables import NetworkTables


class CameraServo:
    

    # speed is tunable via NetworkTables
  #  shoot_speed = tunable(1.0)
    fov = 70
    rest = (180-fov)/2
    turnAngle = fov/2 + rest/2
    #if fov < rest => turn 2 times


    def __init__(self):
        self.sd = NetworkTables.getTable('/SmartDashboard')

        #servo
        self.leftServo = wpilib.Servo(0)
        self.rightServo = wpilib.Servo(1)
        self.leftServo.set(0)
        self.rightServo.set(0)

        #camera stuff
        self.leftCam = self.sd.getAutoUpdateValue('LeftCam',False)
        self.rightCam = self.sd.getAutoUpdateValue('RightCam',False)
        #self.goalFound = self.sd.getAutoUpdateValue('GoalFound',False)

    def enable(self):
        '''Causes the shooter motor to spin'''
        self.enabled = True
    def reset(self):
        self.leftServo.setAngle(0)
        self.rightServo.setAngle(0)
       
    def computeRightCamAngle(self,servoAngle,tagAngle):
        return (servoAngle - tagAngle)

    def computeLeftCamAngle(self,servoAngle,tagAngle):
        angle = 180 + servoAngle - tagAngle
        if (angle > 180):
            angle = -360 + angle
        return angle
  
    def whateverRIGHT(self):
        if (self.rightCam.value):
            angle = self.computeRightCamAngle(self.rightServo.getAngle(), self.rightCam.value)
            self.sd.putNumber("RotateAngle",angle)
            return True
        else:
            self.rightServo.set(45)
            if (self.rightCam.value):
                angle = self.computeRightCamAngle(self.rightServo.getAngle(), self.rightCam.value)
                self.sd.putNumber("RotateAngle",angle)
                return True
            else:
                self.rightServo.set(90)
                if (self.rightCam.value):
                    angle = self.computeRightCamAngle(self.rightServo.getAngle(), self.rightCam.value)
                    self.sd.putNumber("RotateAngle",angle)
                    return True
                else:
                    self.rightServo.set(-45)
                    if (self.rightCam.value):
                        angle = self.computeRightCamAngle(self.rightServo.getAngle(), self.rightCam.value)
                        self.sd.putNumber("RotateAngle",angle)
                        return True 
                    else:
                        self.rightServo.set(-90)
                        if (self.rightCam.value):
                            angle = self.computeRightCamAngle(self.rightServo.getAngle(), self.rightCam.value)
                            self.sd.putNumber("RotateAngle",angle)
                            return True
                        else:
                            return False

    def whateverLEFT(self):
        if (self.leftCam.value):
            angle = self.computeLeftCamAngle(self.leftServo.getAngle(), self.leftCam.value)
            self.sd.putNumber("RotateAngle",angle)
            return True
        else:
            self.leftServo.set(45)
            if (self.leftCam.value):
                angle = self.computeLeftCamAngle(self.leftServo.getAngle(), self.leftCam.value)
                self.sd.putNumber("RotateAngle",angle)
                return True
            else:
                self.leftServo.set(90)
                if (self.leftCam.value):
                    angle = self.computeLeftCamAngle(self.leftServo.getAngle(), self.leftCam.value)
                    self.sd.putNumber("RotateAngle",angle)
                    return True
                else:
                    self.leftServo.set(-45)
                    if (self.leftCam.value):
                        angle = self.computeLeftCamAngle(self.leftServo.getAngle(), self.leftCam.value)
                        self.sd.putNumber("RotateAngle",angle)
                        return True 
                    else:
                        self.leftServo.set(-90)
                        if (self.leftCam.value):
                            angle = self.computeLeftCamAngle(self.leftServo.getAngle(), self.leftCam.value)
                            self.sd.putNumber("RotateAngle",angle)
                            return True
                        else:
                            return False


    def findGoal(self):       
        
        if (self.whateverRIGHT()):
            self.sd.putBoolean('YesTurn', True)
        else:
            if(self.whateverRIGHT()):
                self.sd.putBoolean('YesTurn', True)
        
    def isGoalInSight(self):
        if(self.rightCam.value):
            return True
        return False
    def execute(self):
        '''This gets called at the end of the control loop'''
        #wpilib.Timer.delay(0.005)
        self.update_sd()

    def update_sd(self):
        self.sd.putNumber('LeftServo',self.leftServo.getAngle())
        self.sd.putNumber('RightServo',self.rightServo.getAngle())
