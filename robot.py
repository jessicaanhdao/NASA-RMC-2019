import magicbot
import wpilib
import ctre
#from ctre import WPI_TalonSRX
from wpilib import drive
from components.drive import Drive
from components.scoop import Scoop
from components.depth import Depth
from components.dump import Dump
from components.camera import Camera
from components.cameraservo import CameraServo

import navx
from networktables import NetworkTables

class myRobot(magicbot.MagicRobot):
    drive : Drive
    scoop : Scoop
    depth: Depth
    dump : Dump
    camera : Camera
    servo: CameraServo

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
        """ Set motors """
        self.ldrive_motor = ctre.WPI_TalonSRX(1)
        self.rdrive_motor = ctre.WPI_TalonSRX(2)
        self.scoop_motor = ctre.WPI_TalonSRX(3)
        self.depth_motor = ctre.WPI_TalonSRX(4)
        self.dump_motor = ctre.WPI_TalonSRX(5)
        
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
        self.depth_motor.configSelectedFeedbackSensor(ctre.WPI_TalonSRX.FeedbackDevice.CTRE_MagEncoder_Relative,
            self.kPIDLoopIdx,
            self.kTimeoutMs)
        self.dump_motor.configSelectedFeedbackSensor(ctre.WPI_TalonSRX.FeedbackDevice.CTRE_MagEncoder_Relative,
            self.kPIDLoopIdx,
            self.kTimeoutMs)

        # choose to ensure sensor is positive when output is positive
        self.ldrive_motor.setSensorPhase(True)
        self.rdrive_motor.setSensorPhase(True)

        # pick CW versus CCW when motor controller is positive/green
        self.ldrive_motor.setInverted(True)
        self.rdrive_motor.setInverted(False)
            
        if wpilib.RobotBase.isSimulation():
            print("sim")
            #self.ldrive_motor.setInverted(True)
            #self.rdrive_motor.setInverted(False)
            #_talon0.setInverted(false); // pick CW versus CCW when motor controller is positive/green



        # choose based on what direction you want forward/positive to be.
        # This does not affect sensor phase.
        #self.ldrive_motor.setInverted(False)
        #self.rdrive_motor.setInverted(False)

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

        # zero the sensor
        self.ldrive_motor.setSelectedSensorPosition(0, self.kPIDLoopIdx, self.kTimeoutMs)
        self.rdrive_motor.setSelectedSensorPosition(0, self.kPIDLoopIdx, self.kTimeoutMs)

        self.arcadedrive = wpilib.drive.DifferentialDrive(self.ldrive_motor,self.rdrive_motor)
        self.stick = wpilib.XboxController(1)
        self.timer = wpilib.Timer()
        
        '''# Add the PID Controller to the Test-mode dashboard, allowing manual  */
        # tuning of the Turn Controller's P, I and D coefficients.            */
        # Typically, only the P value needs to be modified.                   */
        wpilib.LiveWindow.addActuator("DriveSystem", "RotateController", turnController)'''

        
        
        #wpilib.CameraServer.launch('vision.py:main')

       # Initialize SmartDashboard, the table of robot values
        self.sd = NetworkTables.getTable('vision') 

        
        ''' turnnController = wpilib.PIDController(
            self.kP, self.kI, self.kD, self.kF, self.ahrs, output=self
        )
        turnnController.setInputRange(-180.0, 180.0)
        turnnController.setOutputRange(-0.1, 0.1)
        turnnController.setAbsoluteTolerance(self.kToleranceDegrees)
        turnnController.setContinuous(True)

        self.turnController = turnnController
        self.turnController.reset()'''

    def teleopPeriodic(self):
        self.timer.start()
        #print("NavX Gyro", self.ahrs.getYaw(), self.ahrs.getAngle())
        self.drive.drive_forward(self.stick.getY())
        # print("y stick: ",self.stick.getY())
        self.drive.rotate(self.stick.getX())
        #self.timer.delay(0.005)

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
        self.depth_motor.disable()
        self.dump_motor.disable()

if __name__ == '__main__':
    wpilib.run(myRobot)