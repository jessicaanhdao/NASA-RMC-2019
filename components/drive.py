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
    
class Drive:    
    ldrive_motor = ctre.WPI_TalonSRX
    rdrive_motor = ctre.WPI_TalonSRX
    arcadedrive = wpilib.drive.DifferentialDrive
    sd = NetworkTables
    target = ntproperty("/camera/target", (0.0, float("inf"), 0.0))


    def __init__(self):
        self.enabled = False
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

        self.kToleranceDegrees = 0.0

        #navx stuff
        self.navX = navx.AHRS.create_spi()
        self.navX.reset()
        self.y = 0
        self.rotationRate = 0
        self.squaredInputs = False
        
        #self.goalFound = self.sd.getAutoUpdateValue('GoalFound',False)
        
        #encoder stuff
        self.positionMode = False
        
        #servo stuff
        self.servoAngle = self.sd.getAutoUpdateValue('Servo',False) 

        self.dist2Goal = self.sd.getAutoUpdateValue('z position',False)
        self.angle2Goal = self.sd.getAutoUpdateValue('pitch camera',False)

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

        


         # Add the PID Controller to the Test-mode dashboard, allowing manual  */
        # tuning of the Turn Controller's P, I and D coefficients.            */
        # Typically, only the P value needs to be modified.                   */
        wpilib.LiveWindow.addActuator("DriveSystem", "RotateController", self.turnController)
        self.targetAngle = 0
    def enable(self):
        '''Causes the shooter motor to spin'''
        self.enabled = True

    def is_ready(self):
        # in a real robot, you'd be using an encoder to determine if the
        # shooter were at the right speed..
        return True
    
    def return_gyro_angle(self):
        """Returns the gyro angle"""
        self.sd.putNumber('Yaw',self.navX.getYaw())
        return self.navX.getYaw()

    def reset_gyro_angle(self):
        """Resets the gyro angle"""
        self.navX.reset()

    def drive_forward(self,y,squaredInputs=False):
        self.positionMode = False    
        self.y = max(min(-y, 1), -1)
        self.turnController.setSetpoint(0)
        self.turnController.enable()
        
    def gyro_drive(self):
        if (abs(self.targetAngle - self.navX.getAngle()) <= self.kToleranceDegrees):
            return True
        return False

    def meterToTicks(self, meters):
        revolution = meters / (math.pi * WHEEL_DIAMETER)
        ticks = revolution  * 4096 * GEAR_RATIO
        #print("ticks calculated: ",ticks)
        return ticks

    def drive_distance(self, meters):
        #something like talon.getSelectedSensorPosition to return the position of selected sensor
       # self.positionMode = True
        self.positionMode = False
        self.target_position = self.meterToTicks(meters)
        
       
        print("left inverted:",self.ldrive_motor.getInverted())
        print("right inverted:",self.rdrive_motor.getInverted())
        print("left sensor: ", self.ldrive_motor.getSelectedSensorPosition(0))
        print("right sensor: ", self.rdrive_motor.getSelectedSensorPosition(0))
        self.y = .1
        #self.turnController.setSetpoint(0)
        #self.turnController.enable()

    #clockwise rotation around the Z axis is positive
    def rotate(self,angle):
       # self.navX.reset()
        self.positionMode = False
        self.y = 0
        
        self.turnController.setSetpoint(angle)
        self.targetAngle = angle
        self.turnController.enable()


    def isDoneRotation(self):
        if (abs(self.targetAngle - self.navX.getAngle()) <= self.kToleranceDegrees):
            return True
        return False

    def stop(self):
        self.y=0
        self.rotationRate=0

    def isGoalFound(self):
        '''found, timestamp, offset = self.target
        if (found > 0) :
            #return self.goalFound.value
            return True'''
        return self.goalFound.value

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

    

    def align90(self):
        while(self.angle2Goal > 1):
            self.rotate(self.angle2Goal)
        
        

    def execute(self):
        '''This gets called at the end of the control loop''' 
        #print("NavX Gyro", self.navX.getYaw(), self.navX.getAngle())
        print(self.turnController.getError())
        if (not self.positionMode):
            #print("in arcadedrive")
            self.arcadedrive.arcadeDrive(self.y,-self.rotationRate,self.squaredInputs)
            #_talonLeft.set(ControlMode.PercentOutput, joyForward, DemandType.ArbitraryFeedForward, +joyTurn)
            #_talonRght.set(ControlMode.PercentOutput, joyForward, DemandType.ArbitraryFeedForward, -joyTurn)
        else:
            self.ldrive_motor.set(WPI_TalonSRX.ControlMode.Position,self.target_position )
            self.rdrive_motor.set(WPI_TalonSRX.ControlMode.Position,self.target_position )

       # wpilib.Timer.delay(0.005)

        # by default, the robot shouldn't move
        #self.y = 0
        #self.rotationRate = 0

        
    def update_sd(self):
        self.sd.putValue('Drive/NavX | Yaw', self.navX.getYaw())