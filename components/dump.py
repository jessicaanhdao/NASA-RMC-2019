import ctre
from networktables import NetworkTables

class Dump:
    dump_motor: ctre.WPI_TalonSRX

    # speed is tunable via NetworkTables
  #  shoot_speed = tunable(1.0)

    def __init__(self):
        self.enabled = False
        NetworkTables.initialize(server='roborio-190-frc.local')
        self.sd = NetworkTables.getTable('/SmartDashboard')
        self.isReadToDump = self.sd.getAutoUpdateValue("IsReadToDump",False)
        self.power = 0
    def enable(self):
        '''Causes the shooter motor to spin'''
        self.enabled = True

    def is_ready(self):
        # in a real robot, you'd be using an encoder to determine if the
        # shooter were at the right speed..
        if(self.isReadToDump):
            return True

    def start_dumping(self):
        self.power = 1

    ''' this is for teleop'''    
    def run(self, power):
        self.power = power

    def execute(self):
        '''This gets called at the end of the control loop'''
        self.dump_motor.set(ctre.WPI_TalonSRX.ControlMode.PercentOutput,self.power)
        pass