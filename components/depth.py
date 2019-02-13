import ctre

class Depth:
    depth_motor: ctre.WPI_TalonSRX

    # speed is tunable via NetworkTables
  #  shoot_speed = tunable(1.0)

    def __init__(self):
        self.enabled = False
        self.power = 1

    def enable(self):
        '''Causes the shooter motor to spin'''
        self.enabled = True

    def is_ready(self):
        # in a real robot, you'd be using an encoder to determine if the
        # shooter were at the right speed..
        return True

    def extend_down(self):
        return True
    
    def unextend_depth(self):
        self.power = -1
        return True

    def execute(self):
        '''This gets called at the end of the control loop'''
        self.depth_motor.set(ctre.WPI_TalonSRX.ControlMode.PercentOutput,self.power)
        self.enabled = False