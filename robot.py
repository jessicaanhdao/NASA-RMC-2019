import magicbot
import wpilib
import ctre
#from ctre import WPI_TalonSRX
from wpilib import drive
from components.drive import Drive
from components.scoop import Scoop
from components.extender import Extender
from components.dump import Dump
from components.cameraservo import CameraServo
from components.bumpswitch import BumpSwitch

import navx
from networktables import NetworkTables

class myRobot(magicbot.MagicRobot):
    drive : Drive
    scoop : Scoop
    extender: Extender
    dump : Dump
    servo: CameraServo
    bumpswitch : BumpSwitch

    #: Which PID slot to pull gains from. Starting 2018, you can choose from
    #: 0,1,2 or 3. Only the first two (0,1) are visible in web-based
    #: configuration.
    kSlotIdx = 0

    #: Talon SRX/ Victor SPX will supported multiple (cascaded) PID loops. For
    #: now we just want the primary one.
    kPIDLoopIdx = 0

    #: set to zero to skip waiting for confirmation, set to nonzero to wait and
    #: report to DS if action fails.
    kTimeoutMs = 10

    #ahrs = navx.AHRS.create_spi()
    currentRotationRate = 0
    kP = 0.05
    kI = 0.1001
    kD = 0.10
    kF = 0.0
    kToleranceDegrees = 0.0

    def createObjects(self):
        self.robot = self
        """ Set motors """
        self.ldrive_motor = ctre.WPI_TalonSRX(1)
        self.rdrive_motor = ctre.WPI_TalonSRX(2)
        self.scoop_motor = ctre.WPI_TalonSRX(3)
        self.extender_motor = ctre.WPI_TalonSRX(4)
        self.dump_motor = ctre.WPI_TalonSRX(5)
    
        """ bump switch """
        self.left_bump = wpilib.DigitalInput(0)
        self.right_bump = wpilib.DigitalInput(1)
        
        """ Set encoders """
        self.ldrive_motor.configSelectedFeedbackSensor(ctre.WPI_TalonSRX.FeedbackDevice.CTRE_MagEncoder_Relative,
            self.kPIDLoopIdx,
            self.kTimeoutMs)
        self.rdrive_motor.configSelectedFeedbackSensor(ctre.WPI_TalonSRX.FeedbackDevice.CTRE_MagEncoder_Relative,
            self.kPIDLoopIdx,
            self.kTimeoutMs)
        self.scoop_motor.configSelectedFeedbackSensor(ctre.WPI_TalonSRX.FeedbackDevice.CTRE_MagEncoder_Relative,
            self.kPIDLoopIdx,
            self.kTimeoutMs)
        '''self.extender_motor.configSelectedFeedbackSensor(ctre.WPI_TalonSRX.FeedbackDevice.CTRE_MagEncoder_Relative,
            self.kPIDLoopIdx,
            self.kTimeoutMs)
        self.dump_motor.configSelectedFeedbackSensor(ctre.WPI_TalonSRX.FeedbackDevice.CTRE_MagEncoder_Relative,
            self.kPIDLoopIdx,
            self.kTimeoutMs)'''

        '''left is forward, green light when drive forward, right is reverse'''
        ''' likely to be, left = true, right = false. true = pos encoder when moving forward'''
        # choose to ensure sensor is positive when output is positive
        #self.ldrive_motor.setSensorPhase(True)
        #self.rdrive_motor.setSensorPhase(False)


        # pick CW versus CCW when motor controller is positive/green
        #self.ldrive_motor.setInverted(False)
        #self.rdrive_motor.setInverted(True)

        self.extender_motor.setInverted(True)
        self.scoop_motor.setInverted(True)
        self.dump_motor.setInverted(True)
            
        if wpilib.RobotBase.isSimulation():
            print("sim")
            #self.ldrive_motor.setInverted(True)
            #self.rdrive_motor.setInverted(False)
            #_talon0.setInverted(false); // pick CW versus CCW when motor controller is positive/green




        # Set relevant frame periods to be at least as fast as periodic rate
        self.ldrive_motor.setStatusFramePeriod(ctre.WPI_TalonSRX.StatusFrameEnhanced.Status_13_Base_PIDF0, 10, self.kTimeoutMs)
        self.ldrive_motor.setStatusFramePeriod(ctre.WPI_TalonSRX.StatusFrameEnhanced.Status_10_MotionMagic, 10, self.kTimeoutMs)
        self.rdrive_motor.setStatusFramePeriod(ctre.WPI_TalonSRX.StatusFrameEnhanced.Status_13_Base_PIDF0, 10, self.kTimeoutMs)
        self.rdrive_motor.setStatusFramePeriod(ctre.WPI_TalonSRX.StatusFrameEnhanced.Status_10_MotionMagic, 10, self.kTimeoutMs)
        # set the peak and nominal outputs, 12V means full
        '''self.ldrive_motor.configNominalOutputForward(0, self.kTimeoutMs)
        self.ldrive_motor.configNominalOutputReverse(0, self.kTimeoutMs)
        self.ldrive_motor.configPeakOutputForward(1, self.kTimeoutMs)
        self.ldrive_motor.configPeakOutputReverse(-1, self.kTimeoutMs)

        self.rdrive_motor.configNominalOutputForward(0, self.kTimeoutMs)
        self.rdrive_motor.configNominalOutputReverse(0, self.kTimeoutMs)
        self.rdrive_motor.configPeakOutputForward(1, self.kTimeoutMs)
        self.rdrive_motor.configPeakOutputReverse(-1, self.kTimeoutMs)'''

        # Set the allowable closed-loop error, Closed-Loop output will be
        # neutral within this range. See Table in Section 17.2.1 for native
        # units per rotation.
        self.ldrive_motor.configAllowableClosedloopError(0, self.kPIDLoopIdx, self.kTimeoutMs)
        self.rdrive_motor.configAllowableClosedloopError(0, self.kPIDLoopIdx, self.kTimeoutMs)
        self.extender_motor.configAllowableClosedloopError(0, self.kPIDLoopIdx, self.kTimeoutMs)

        # set closed loop gains in slot0, typically kF stays zero - see documentation */
        self.ldrive_motor.selectProfileSlot(self.kSlotIdx, self.kPIDLoopIdx)
        self.ldrive_motor.config_kF(0, 0, self.kTimeoutMs)
        self.ldrive_motor.config_kP(0, 0.1, self.kTimeoutMs)
        self.ldrive_motor.config_kI(0, 0, self.kTimeoutMs)
        self.ldrive_motor.config_kD(0, 0, self.kTimeoutMs)

        self.rdrive_motor.selectProfileSlot(self.kSlotIdx, self.kPIDLoopIdx)
        self.rdrive_motor.config_kF(0, 0, self.kTimeoutMs)
        self.rdrive_motor.config_kP(0, 0.1, self.kTimeoutMs)
        self.rdrive_motor.config_kI(0, 0, self.kTimeoutMs)
        self.rdrive_motor.config_kD(0, 0, self.kTimeoutMs)

        self.extender_motor.selectProfileSlot(self.kSlotIdx, self.kPIDLoopIdx)
        self.extender_motor.config_kF(0, 0, self.kTimeoutMs)
        self.extender_motor.config_kP(0, 0.1, self.kTimeoutMs)
        self.extender_motor.config_kI(0, 0, self.kTimeoutMs)
        self.extender_motor.config_kD(0, 0, self.kTimeoutMs)

        # zero the sensor
        self.ldrive_motor.setSelectedSensorPosition(0, self.kPIDLoopIdx, self.kTimeoutMs)
        self.rdrive_motor.setSelectedSensorPosition(0, self.kPIDLoopIdx, self.kTimeoutMs)
        self.extender_motor.setSelectedSensorPosition(0, self.kPIDLoopIdx, self.kTimeoutMs)


        self.arcadedrive = wpilib.drive.DifferentialDrive(self.ldrive_motor,self.rdrive_motor)
        self.stick = wpilib.XboxController(1)
        self.timer = wpilib.Timer()
        
        '''# Add the PID Controller to the Test-mode dashboard, allowing manual  */
        # tuning of the Turn Controller's P, I and D coefficients.            */
        # Typically, only the P value needs to be modified.                   */
        wpilib.LiveWindow.addActuator("DriveSystem", "RotateController", turnController)'''

        
        
        #wpilib.CameraServer.launch('vision.py:main')

        '''Initialize SmartDashboard, the table of robot values'''
        self.sd = NetworkTables.getTable('SmartDashboard') 



    def teleopPeriodic(self):
        self.timer.start()
        #print("NavX Gyro", self.ahrs.getYaw(), self.ahrs.getAngle())
        if (not self.stick.getRawButton(1) and not self.stick.getRawButton(2) and not self.stick.getRawButton(3)  ):
            self.drive.run(-self.stick.getY(hand=wpilib.XboxController.Hand.kLeft), -self.stick.getY())
        #print("drive: ",self.stick.getY(), self.stick.getX() )
        '''kA = 1
        kB = 2
        kX = 3
        kY = 4
        A button -- run extender
        B button -- run scoop
        X button -- run dump'''
        if (self.stick.getRawButton(1) ):
            self.extender.run(-self.stick.getY())
        if ( self.stick.getRawButton(2)  ):
            self.scoop.run(-self.stick.getY())
        if (self.stick.getRawButton(3)):
            self.dump.run(-self.stick.getY())
            

        

        '''   def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""
        self.timer.reset()
        self.timer.start()'''

    def autonomous(self):    
      #  self.arcadedrive.setSafetyEnabled(False)
        """This function is called periodically during autonomous."""
        self.timer.reset()
        self.timer.start()

        magicbot.MagicRobot.autonomous(self)

        """# Drive for two seconds
        if self.timer.get() < 10.0:
            self.drive.arcadeDrive(-0.5, 0)  # Drive forwards at half speed
        else:
            self.drive.arcadeDrive(0, 0)  # Stop robot"""

    def disabledPeriodic(self):
        self.ldrive_motor.disable()
        self.rdrive_motor.disable()
        self.scoop_motor.disable()
        self.extender_motor.disable()
        self.dump_motor.disable()

if __name__ == '__main__':
    wpilib.run(myRobot)