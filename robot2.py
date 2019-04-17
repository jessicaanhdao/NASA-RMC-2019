import magicbot
import wpilib
import ctre
from wpilib import drive

class myRobot(wpilib.TimedRobot):
    def robotInit(self):
        """ Set motors """
        self.ldrive_motor = ctre.WPI_TalonSRX(1)
        self.rdrive_motor = ctre.WPI_TalonSRX(2)
        self.scoop_motor = ctre.WPI_TalonSRX(3)
        self.extender_motor = ctre.WPI_TalonSRX(4)
        self.dump_motor = ctre.WPI_TalonSRX(5)
        
        """ Set encoders """
        self.ldrive_motor.configSelectedFeedbackSensor(ctre.WPI_TalonSRX.FeedbackDevice.QuadEncoder)
        self.rdrive_motor.configSelectedFeedbackSensor(ctre.WPI_TalonSRX.FeedbackDevice.QuadEncoder)
        self.scoop_motor.configSelectedFeedbackSensor(ctre.WPI_TalonSRX.FeedbackDevice.QuadEncoder)
        self.extender_motor.configSelectedFeedbackSensor(ctre.WPI_TalonSRX.FeedbackDevice.QuadEncoder)
        self.dump_motor.configSelectedFeedbackSensor(ctre.WPI_TalonSRX.FeedbackDevice.QuadEncoder)

        self.drive = wpilib.drive.DifferentialDrive(self.ldrive_motor,self.rdrive_motor)
        
        self.stick = wpilib.XboxController(1)
       #self.reverseButton = ButtonDebouncer(self.stick, 1)

        self.timer = wpilib.Timer()

    def teleopPeriodic(self):
        #self.drive.tankDrive(1,1)
        self.drive.tankDrive(self.stick.getY(hand=wpilib.XboxController.Hand.kLeft), self.stick.getY(), False)
        #self.ldrive_motor.set(ctre.WPI_TalonSRX.ControlMode.PercentOutput, self.stick.getY()/10)
#       self.rdrive_motor.set(ctre.WPI_TalonSRX.ControlMode.PercentOutput, self.stick.getX())

        """press button A"""
        if (self.stick.getRawButton(1)):
            self.scoop_motor.set(ctre.WPI_TalonSRX.ControlMode.PercentOutput,self.stick.getY())

        """press button B"""
        if (self.stick.getRawButton(2)):
            self.ldrive_motor.set(ctre.WPI_TalonSRX.ControlMode.PercentOutput, self.stick.getY())


    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""
        self.timer.reset()
        self.timer.start()

    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""

        # Drive for two seconds
        if self.timer.get() < 10.0:
            self.drive.arcadeDrive(-0.5, 0)  # Drive forwards at half speed
        else:
            self.drive.arcadeDrive(0, 0)  # Stop robot

    def disabledPeriodic(self):
        self.ldrive_motor.disable()
        self.rdrive_motor.disable()
        self.scoop_motor.disable()
        self.extender_motor.disable()
        self.dump_motor.disable()

if __name__ == '__main__':
    wpilib.run(myRobot)