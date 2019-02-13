import ctre, wpilib
from ctre import WPI_TalonSRX
from networktables import NetworkTables
import logging
import navx
#from wpilib import drive

class Drive:
    ldrive_motor = ctre.WPI_TalonSRX
    rdrive_motor = ctre.WPI_TalonSRX
    #tankdrive = wpilib.drive.DifferentialDrive
    arcadedrive = wpilib.drive.DifferentialDrive
    #navX = navx.AHRS
    sd = NetworkTables
    ''' self.kP = 0.03
    self.kI = 0.00
    self.kD = 0.00
    self.kF = 0.00

    self.kToleranceDegrees = 2.0
    turnController = wpilib.PIDController'''

    # speed is tunable via NetworkTables
   # shoot_speed = tunable(1.0)

    def __init__(self):
        self.enabled = False
        self.sd = NetworkTables.getTable('/SmartDashboard')
        if wpilib.RobotBase.isSimulation():
            # These PID parameters are used in simulation
            self.kP = 0.10
            self.kI = 0.010
            self.kD = 0.020
            self.kF = 0.00
            print("Is simulation")
        else:    
            self.kP = 0.04
            self.kI = 0.001
            self.kD = 0.020
            self.kF = 0.00
            print("Is not simulation")

        self.kToleranceDegrees = 2.0

        self.navX = navx.AHRS.create_spi()
        self.y = 0
        self.rotationRate = 0
        self.squaredInputs = False
        self.goalFound = self.sd.getAutoUpdateValue('ObjectFound',False)
       # self.navxYaw = self.sd.getAutoUpdateValue('Yaw',0)

        self.turnController = wpilib.PIDController(
            self.kP, self.kI, self.kD, self.kF, self.navX, output=self
        )
        self.turnController.setInputRange(-180.0, 180.0)
        self.turnController.setOutputRange(-0.2, 0.2)
        self.turnController.setAbsoluteTolerance(self.kToleranceDegrees)
        self.turnController.setContinuous(True)

        #self.turnController = turnController
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
            self.y = max(min(-y, 1), -1)
            self.turnController.enable()
            self.turnController.setSetpoint(0)
            self.rotationRate = self.rotateToAngleRate
            #self.rotationRate = max(min(1.0, self.rotationRate), -1)
            self.squaredInputs = squaredInputs

            '''test Motion Magic'''
            # Motion Magic - 4096 ticks/rev * 10 Rotations in either direction
         
        #else:
        #    self.y = 0
        #    self.rotationRate = 0

    def rotate(self,angle):
        self.navX.reset()
        self.turnController.setSetpoint(angle)
        self.turnController.enable()
        self.targetAngle = angle
     #   self.rotationRate = angle
        
    def pidWrite(self, output):
        """This function is invoked periodically by the PID Controller,
        based upon navX MXP yaw angle input and PID Coefficients.
        """
        print("Output: ",output)
        self.rotateToAngleRate = output

    def execute(self):
        '''This gets called at the end of the control loop''' 
        self.rotationRate = self.rotateToAngleRate
        print("rotationRate: ",self.rotationRate)
        self.arcadedrive.arcadeDrive(self.y,self.rotationRate,self.squaredInputs)
        if (self.navX.getAngle == self.targetAngle - self.kToleranceDegrees):
            self.arcadedrive.arcadeDrive(0,0,False)
        print("NavX Gyro: ", self.navX.getYaw(), self.navX.getAngle())
      #  wpilib.Timer.delay(0.05)

        # by default, the robot shouldn't move
        self.y = 0
        self.rotation = 0
        
    def update_sd(self):
        self.sd.putValue('Drive/NavX | Yaw', self.navX.getYaw())
