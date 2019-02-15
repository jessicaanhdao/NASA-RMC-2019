import ctre, wpilib
from ctre import WPI_TalonSRX
from networktables import NetworkTables
import logging
import navx
#from wpilib import drive

class Drive:
    ENCODER_ROTATION = 1023
    WHEEL_DIAMETER = 7.639
    
    ldrive_motor = ctre.WPI_TalonSRX
    rdrive_motor = ctre.WPI_TalonSRX
    arcadedrive = wpilib.drive.DifferentialDrive
    sd = NetworkTables
    

    def __init__(self):
        self.enabled = False
        self.sd = NetworkTables.getTable('/SmartDashboard')
        if wpilib.RobotBase.isSimulation():
            # These PID parameters are used in simulation
            self.kP = 0.5
            self.kI = 0.01
            self.kD = 2.0
            self.kF = 0.0
            print("Is simulation")
        else:    
            self.kP = 0.04
            self.kI = 0.01
            self.kD = 0.020
            self.kF = 0.00
            print("Is not simulation")

        self.kToleranceDegrees = 4.0

        self.navX = navx.AHRS.create_spi()
        self.navX.reset()
        self.y = 0
        self.rotationRate = 0
        self.squaredInputs = False
        self.goalFound = self.sd.getAutoUpdateValue('ObjectFound',False)
       # self.navxYaw = self.sd.getAutoUpdateValue('Yaw',0)

        turnController = wpilib.PIDController(
            self.kP, self.kI, self.kD, self.kF, self.navX, output=self
        )
        turnController.setInputRange(-180.0, 180.0)
        turnController.setOutputRange(-0.15, 0.15)
        turnController.setAbsoluteTolerance(self.kToleranceDegrees)
        turnController.setContinuous(True)

        self.turnController = turnController
        self.turnController.reset()
        self.rotateToAngleRate = 0
         # Add the PID Controller to the Test-mode dashboard, allowing manual  */
        # tuning of the Turn Controller's P, I and D coefficients.            */
        # Typically, only the P value needs to be modified.                   */
        wpilib.LiveWindow.addActuator("DriveSystem", "RotateController", self.turnController)

        '''Motion Magic'''

       
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
        #if(self.goalFound.value):
           # self.navX.reset()
            self.y = max(min(-y, 1), -1)
            self.turnController.setSetpoint(0)
            self.turnController.enable()
            
            #self.rotationRate = 0

        #else:
        #    self.y = 0
        #    self.rotationRate = 0
    def gyro_drive(self):
        if (abs(self.targetAngle - self.navX.getAngle()) <= self.kToleranceDegrees):
            return True
        return False
    def rotate(self,angle):
       # self.navX.reset()
        self.y = 0
        
        self.turnController.setSetpoint(-angle)
        self.targetAngle = angle
        self.turnController.enable()
        print("rotationRate: ",self.rotationRate)
        return self.gyro_drive()
     #   self.rotationRate = angle
        
    def pidWrite(self, output):
        """This function is invoked periodically by the PID Controller,
        based upon navX MXP yaw angle input and PID Coefficients.
        """
        print("Output: ",output)
        self.rotationRate = output

    def execute(self):
        '''This gets called at the end of the control loop''' 
        
        self.arcadedrive.arcadeDrive(self.y,self.rotationRate,self.squaredInputs)
        
        print("NavX Gyro: ", self.navX.getYaw(), self.navX.getAngle())
        wpilib.Timer.delay(0.005)

        # by default, the robot shouldn't move
        #self.y = 0
        #self.rotationRate = 0

        
    def update_sd(self):
        self.sd.putValue('Drive/NavX | Yaw', self.navX.getYaw())