<<<<<<< HEAD
import ctre

class Scoop:
    scoop_motor: ctre.WPI_TalonSRX

    # speed is tunable via NetworkTables
  #  shoot_speed = tunable(1.0)

    def __init__(self):
        self.enabled = False

    def enable(self):
        '''Causes the shooter motor to spin'''
        self.enabled = True

    def is_ready(self):
        # in a real robot, you'd be using an encoder to determine if the
        # shooter were at the right speed..
        return True

    def scoop_down(self):
        return True

    def execute(self):
        '''This gets called at the end of the control loop'''
        self.scoop_motor.set(ctre.WPI_TalonSRX.ControlMode.PercentOutput,1)
=======
import ctre

class Scoop:
    scoop_motor: ctre.WPI_TalonSRX

    # speed is tunable via NetworkTables
  #  shoot_speed = tunable(1.0)

    def __init__(self):
        self.enabled = False

    def enable(self):
        '''Causes the shooter motor to spin'''
        self.enabled = True

    def is_ready(self):
        # in a real robot, you'd be using an encoder to determine if the
        # shooter were at the right speed..
        return True

    def scoop_down(self):
        return True

    def execute(self):
        '''This gets called at the end of the control loop'''
        self.scoop_motor.set(ctre.WPI_TalonSRX.ControlMode.PercentOutput,1)
>>>>>>> remotes/origin/master
        self.enabled = False