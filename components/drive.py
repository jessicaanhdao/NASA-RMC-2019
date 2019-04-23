import ctre, wpilib, math
import wpilib.command.pidsubsystem
from ctre import WPI_TalonSRX
from networktables import NetworkTables
import logging
import navx
from networktables.util import ntproperty
#import wpilib.servo as servo

#from wpilib import drive

ENCODER_ROTATION = 4096
WHEEL_CIRCUMFERENCE = 2.31
WHEEL_DIAMETER = 0.08 #meter
GEAR_RATIO = 75
    
#NetworkTables.initialize(server=ip)

class Drive:    
    ldrive_motor : ctre.WPI_TalonSRX
    rdrive_motor : ctre.WPI_TalonSRX
    arcadedrive : wpilib.drive.DifferentialDrive
    sd = NetworkTables
    #target = ntproperty("/camera/target", (0.0, float("inf"), 0.0))
    #: Talon SRX/ Victor SPX will supported multiple (cascaded) PID loops. For
    #: now we just want the primary one.
    kPIDLoopIdx = 0

    #: set to zero to skip waiting for confirmation, set to nonzero to wait and
    #: report to DS if action fails.
    kTimeoutMs = 10
    def __init__(self):
        self.enabled = False
        NetworkTables.initialize(server='roborio-190-frc.local')
        self.sd = NetworkTables.getTable('/SmartDashboard')
        if wpilib.RobotBase.isSimulation():
            # These PID parameters are used in simulation
            self.kP = 0.05
            self.kI = 0.0
            self.kD = 0.00
            self.kF = 0.0
            print("Is simulation")
        else:    
            self.kP = 0.04
            self.kI = 0.01
            self.kD = 0.020
            self.kF = 0.00
            print("Is not simulation")

        self.kToleranceDegrees = 2.0

        #navx stuff
        self.navX = navx.AHRS.create_spi()
        self.navX.reset()
        self.y = 0
        self.rotationRate = 0
        self.squaredInputs = False

        #encoder stuff
        self.positionMode = False
        
        #servo stuff
        self.yesTurn = self.sd.getAutoUpdateValue("YesTurn",False)
        self.rotateAngle = self.sd.getAutoUpdateValue("RotateAngle",0)
        self.leftServo = self.sd.getAutoUpdateValue("LeftServo",0)
        self.rightServo = self.sd.getAutoUpdateValue("RightServo",0)
       
        #digging stuff
        self.MoveBackwardToDig = self.sd.getAutoUpdateValue("MoveBackwardToDig",False)
        self.digging = self.sd.getAutoUpdateValue('Digging','Nothing')

        #bump switch stuff
        self.leftBump = self.sd.getAutoUpdateValue("LeftBump",True)
        self.rightBump = self.sd.getAutoUpdateValue("RightBump",True)
        self.dockingMode = False
        self.leftPower = 0
        self.rightPower = 0

        #camera stuff
        self.tagAngle = self.sd.getAutoUpdateValue("TagAngle",0)
        self.leftCam = self.sd.getAutoUpdateValue('LeftCam',False)
        self.rightCam = self.sd.getAutoUpdateValue('RightCam',False)
        self.tagDistance = self.sd.getAutoUpdateValue('TagDistance',0)
        
        #PID for NAVX
        turnController = wpilib.PIDController(
            self.kP, self.kI, self.kD, self.kF, self.navX, output=self
        )
        turnController.setInputRange(-180.0, 180.0)
        turnController.setOutputRange(-0.1, 0.1)
        turnController.setAbsoluteTolerance(self.kToleranceDegrees)
        turnController.setContinuous(True)
        self.turnController = turnController
        self.turnController.reset()
        self.rotateToAngleRate = 0
        
        self.timer = wpilib.Timer()
        self.timer.start()
        


        # Add the PID Controller to the Test-mode dashboard, allowing manual  */
        # tuning of the Turn Controller's P, I and D coefficients.            */
        # Typically, only the P value needs to be modified.                   */
        self.targetAngle = 0
    
    def return_gyro_angle(self):
        """Returns the gyro angle"""
        return self.navX.getYaw()

    def resetNavx(self):
        """Resets the gyro angle"""
        self.navX.reset()
    
    def resetEncoder(self):
        self.ldrive_motor.setSelectedSensorPosition(0, self.kPIDLoopIdx, self.kTimeoutMs)
        self.rdrive_motor.setSelectedSensorPosition(0, self.kPIDLoopIdx, self.kTimeoutMs)

    def drive(self,y,squaredInputs=False):
        #if (self.MoveBackwardToDig and self.digging.value != 'Nothing'):
        #    self.y=0
        #else:
            self.positionMode = False   
            self.dockingMode = False 
            self.y = y
            self.turnController.setSetpoint(0)
            self.turnController.enable()
            print("Still driving",self.timer.get())
        
    '''def gyro_drive(self):
        if (abs(self.targetAngle - self.navX.getAngle()) <= self.kToleranceDegrees):
            return True
        return False'''

    def meterToTicks(self, meters):
        revolution = meters / (math.pi * WHEEL_DIAMETER)
        ticks = revolution  * ENCODER_ROTATION * GEAR_RATIO
        #print("ticks calculated: ",ticks)
        return ticks

    def ticksToMeter(self, ticks):
        meters = ticks *(math.pi * WHEEL_DIAMETER) /(ENCODER_ROTATION * GEAR_RATIO)
        return meters

    def drive_distance(self, meters):
        self.positionMode = True
        self.dockingMode = False
        self.target_position = self.meterToTicks(meters)

        '''print("left inverted:",self.ldrive_motor.getInverted())
        print("right inverted:",self.rdrive_motor.getInverted())
        print("left sensor: ", self.ldrive_motor.getSelectedSensorPosition(0))
        print("right sensor: ", self.rdrive_motor.getSelectedSensorPosition(0))'''
        #self.y = 1
        self.turnController.setSetpoint(0)
        self.turnController.enable()

    def isDistanceReached(self, meter):
        if (meter - self.ticksToMeter(self.ldrive_motor.getSelectedSensorPosition()) <= 0.1):
            return True
        return False


    #clockwise rotation around the Z axis is positive
    def rotate(self,angle):
       # self.navX.reset()
        self.positionMode = False
        self.dockingMode = False
        self.y = 0
        self.turnController.setSetpoint(angle)
        self.targetAngle = angle
        self.turnController.enable()
        print("Rotating...")

    def isDoneRotating(self):
        if (abs(self.targetAngle - self.navX.getAngle()) <= self.kToleranceDegrees):
            print ("---done rotating---")
            return True 
        return False

    '''  self localization '''
    def rotate2Parallel(self):
        if (self.yesTurn.value):
            angle = self.rotateAngle.value
            self.rotate(angle)

    ''' before docking'''
    def rotate2Perpendicular(self):
        angle = 90 + self.navX.getYaw() # CCW is neg, CW is pos
        self.rotate(angle)

    '''  docking '''
    def dock(self):
        self.positionMode = False
        self.dockingMode = False

        #self.rotate(-90)
        
        while (self.leftBump and self.rightBump):
            self.dockingMode = False
            self.drive(-0.5)
        #remember this is reverse. False is PRESSED, True is NOT PRESSED
        # case 1 : right is PRESSED
        while (self.leftBump and not self.rightBump):
            self.dockingMode = True
            self.leftPower = -0.5
            self.rightPower = 0
        # case 2 : left is PRESSED
        while (not self.leftBump and self.rightBump):
            self.dockingMode = True
            self.leftPower = 0
            self.rightPower = -0.5 #lower power
        if (not self.leftBump and not self.rightBump):
            #STOP or KEEP powering?
            self.drive(-0.1)
            self.sd.putBoolean("IsReadToDump",True)
            

    def stop(self):
        print("drive motor stopped")
        self.y=0
        self.rotationRate=0
        self.arcadedrive.stopMotor()

    
    def isGoalFound(self):
        return self.yesTurn.value
        #return True

    def pidWrite(self, output):
        """This function is invoked periodically by the PID Controller,
        based upon navX MXP yaw angle input and PID Coefficients.
        """
        #print("Output: ",output)
        self.rotationRate = output
        #print out what the input is, make sure that lines up w navx

    def isFrontFacingUp(self):
        if (self.rightCam):
            return True
        else:
            return False
        
    
    ''' this is for teleop'''    
    def run(self, speed, rotation):
        
        self.y = speed
        self.rotationRate = rotation
    
    def execute(self):
        '''This gets called at the end of the control loop''' 
        if (self.positionMode):
            self.ldrive_motor.set(WPI_TalonSRX.ControlMode.Position,self.target_position)
            self.rdrive_motor.set(WPI_TalonSRX.ControlMode.Position,self.target_position)
        elif (self.dockingMode):
            self.ldrive_motor.set(WPI_TalonSRX.ControlMode.PercentOutput,self.leftPower)
            self.rdrive_motor.set(WPI_TalonSRX.ControlMode.PercentOutput,self.rightPower)
        else:
            self.arcadedrive.arcadeDrive(self.y,-self.rotationRate,self.squaredInputs)

        self.update_sd()
            
        
       # wpilib.Timer.delay(0.005)

        # by default, the robot shouldn't move
        #self.y = 0
        #self.rotationRate = 0

        
    def update_sd(self):
        self.sd.putValue('Drive/NavX Yaw', self.navX.getYaw())
        self.sd.putValue('Drive/Left Encoder', self.ldrive_motor.getSelectedSensorPosition())
        self.sd.putValue('Drive/Right Encoder', self.rdrive_motor.getSelectedSensorPosition())