import ctre, wpilib
from networktables import NetworkTables

DELAY = 2
class CameraServo:
    

    # speed is tunable via NetworkTables
  #  shoot_speed = tunable(1.0)
    fov = 70
    rest = (180-fov)/2
    turnAngle = fov/2 + rest/2
    #if fov < rest => turn 2 times
    sd = NetworkTables
    

    def __init__(self):
        self.enabled = False
        NetworkTables.initialize(server='roborio-190-frc.local')
        self.sd = NetworkTables.getTable('/SmartDashboard')

        #servo
        self.leftServo = wpilib.Servo(0)
        self.rightServo = wpilib.Servo(1)
        self.leftServo.set(0)
        self.rightServo.set(0)

        #camera stuff
        self.leftCam = self.sd.getAutoUpdateValue('LeftCamera',False)
        self.rightCam = self.sd.getAutoUpdateValue('RightCamera',False)
        #self.goalFound = self.sd.getAutoUpdateValue('GoalFound',False)

    def enable(self):
        '''Causes the shooter motor to spin'''
        self.enabled = True
        
    def reset(self):
        self.leftServo.setAngle(90)
        self.rightServo.setAngle(90)
       
    def computeRightCamAngle(self,servoAngle,tagAngle):
        return (servoAngle - tagAngle)

    def computeLeftCamAngle(self,servoAngle,tagAngle):
        angle = 180 + servoAngle - tagAngle
        if (angle > 180):
            angle = -360 + angle
        return angle
  
    def justrotate(self):
        print("Left Servo:",self.leftServo.getAngle())
        print("Right Servo:",self.rightServo.getAngle())
        self.leftServo.setAngle(0.0)
        wpilib.Timer.delay(0.5)
        self.leftServo.setAngle(45.0)
        print(" 45Left Servo:",self.leftServo.getAngle())
        print("Right Servo:",self.rightServo.getAngle())
        wpilib.Timer.delay(0.5)
        self.leftServo.setAngle(90.0)
        print("90 Left Servo:",self.leftServo.getAngle())
        print("Right Servo:",self.rightServo.getAngle())
        wpilib.Timer.delay(0.5)
        self.leftServo.setAngle(135)
        print("135 Left Servo:",self.leftServo.getAngle())
        print("Right Servo:",self.rightServo.getAngle())
        wpilib.Timer.delay(0.5)
        self.leftServo.setAngle(180)
        print("180 Left Servo:",self.leftServo.getAngle())
        print("Right Servo:",self.rightServo.getAngle())
        wpilib.Timer.delay(0.5)
        #self.leftServo.setAngle(135)
        #self.leftServo.setAngle(90)
        #self.leftServo.setAngle(45)
        #self.leftServo.setAngle(0)
        self.rightServo.setAngle(0.0)
        wpilib.Timer.delay(0.5)
        self.rightServo.setAngle(45.0)
        wpilib.Timer.delay(0.5)
        self.rightServo.setAngle(90.0)
        wpilib.Timer.delay(0.5)
        self.rightServo.setAngle(135)
        wpilib.Timer.delay(0.5)
        self.rightServo.setAngle(180)
        wpilib.Timer.delay(0.5)
        #self.rightServo.setAngle(135)
        #self.rightServo.setAngle(90)
        #self.rightServo.setAngle(45)
        #self.rightServo.setAngle(0)
    def whateverRIGHT(self):
        self.leftServo.setAngle(0)
        wpilib.Timer.delay(DELAY)
        if (self.rightCam.value):
            angle = self.computeRightCamAngle(self.rightServo.getAngle(), self.rightCam.value)
            self.sd.putNumber("RotateAngle",angle)
            return True
        else:
            self.rightServo.setAngle(45)
            wpilib.Timer.delay(DELAY)
            if (self.rightCam.value):
                angle = self.computeRightCamAngle(self.rightServo.getAngle(), self.rightCam.value)
                self.sd.putNumber("RotateAngle",angle)
                return True
            else:
                self.rightServo.setAngle(90)
                wpilib.Timer.delay(DELAY)
                if (self.rightCam.value):
                    angle = self.computeRightCamAngle(self.rightServo.getAngle(), self.rightCam.value)
                    self.sd.putNumber("RotateAngle",angle)
                    return True
                else:
                    self.rightServo.setAngle(135)
                    wpilib.Timer.delay(DELAY)
                    if (self.rightCam.value):
                        angle = self.computeRightCamAngle(self.rightServo.getAngle(), self.rightCam.value)
                        self.sd.putNumber("RotateAngle",angle)
                        return True 
                    else:
                        self.rightServo.setAngle(180)
                        wpilib.Timer.delay(DELAY)
                        if (self.rightCam.value):
                            angle = self.computeRightCamAngle(self.rightServo.getAngle(), self.rightCam.value)
                            self.sd.putNumber("RotateAngle",angle)
                            return True
                        else:
                            return False

    def whateverLEFT(self):
        self.leftServo.setAngle(0)
        wpilib.Timer.delay(DELAY)
        if (self.leftCam.value):
            angle = self.computeLeftCamAngle(self.leftServo.getAngle(), self.leftCam.value)
            self.sd.putNumber("RotateAngle",angle)
            return True
        else:
            self.leftServo.setAngle(45)
            wpilib.Timer.delay(DELAY)
            if (self.leftCam.value):
                angle = self.computeLeftCamAngle(self.leftServo.getAngle(), self.leftCam.value)
                self.sd.putNumber("RotateAngle",angle)
                return True
            else:
                self.leftServo.setAngle(90)
                wpilib.Timer.delay(DELAY)
                if (self.leftCam.value):
                    angle = self.computeLeftCamAngle(self.leftServo.getAngle(), self.leftCam.value)
                    self.sd.putNumber("RotateAngle",angle)
                    return True
                else:
                    self.leftServo.setAngle(135)
                    wpilib.Timer.delay(DELAY)
                    if (self.leftCam.value):
                        angle = self.computeLeftCamAngle(self.leftServo.getAngle(), self.leftCam.value)
                        self.sd.putNumber("RotateAngle",angle)
                        return True 
                    else:
                        self.leftServo.setAngle(180)
                        wpilib.Timer.delay(DELAY)
                        if (self.leftCam.value):
                            angle = self.computeLeftCamAngle(self.leftServo.getAngle(), self.leftCam.value)
                            self.sd.putNumber("RotateAngle",angle)
                            return True
                        else:
                            return False


    def findGoal(self):       
        #while (not self.leftCam.value and not self.rightCam.value):
            if (self.whateverRIGHT()):
                self.sd.putBoolean('YesTurn', True)
            else:
                if(self.whateverLEFT()):
                    self.sd.putBoolean('YesTurn', True)
        
    def isGoalInSight(self):
        if(self.rightCam.value):
            return True
        return False
    def execute(self):
        print("Left Servo:",self.leftServo.getAngle())
        print("Right Servo:",self.rightServo.getAngle())
        '''This gets called at the end of the control loop'''
        
        self.update_sd()

    def update_sd(self):
        self.sd.putNumber('LeftServo',self.leftServo.getAngle())
        self.sd.putNumber('RightServo',self.rightServo.getAngle())
