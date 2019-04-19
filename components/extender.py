import ctre, math, wpilib
from networktables import NetworkTables
ENCODER_ROTATION = 4096

SHALF_DIAMETER = 0.01 #meter
GEAR_RATIO = 75

class Extender:
    extender_motor: ctre.WPI_TalonSRX

    # speed is tunable via NetworkTables
  #  shoot_speed = tunable(1.0)

    def __init__(self):
        self.enabled = False
        self.power = 0
        NetworkTables.initialize(server='roborio-190-frc.local')
        self.sd = NetworkTables.getTable('/SmartDashboard')
        self.timer = wpilib.Timer()
        self.canExtend = self.sd.getAutoUpdateValue('CanExtend',True)
        self.digging = self.sd.getAutoUpdateValue('Digging','Nothing')
        #position mode
        self.positionMode = False
        self.target_position = 0
        self.kToleranceMeters = 0.05 #meter

    def extend_distance(self,meter):
        self.positionMode = True
        self.target_position = self.meterToTicks(meter)

    def isDistanceReached(self, meter):
        if (meter - self.ticksToMeter(self.extender_motor.getSelectedSensorPosition()) <= self.kToleranceMeters):
            return True
        return False

    def extend_down(self,power):
        self.positionMode = False
        if (self.canExtend.value):
            self.power = power
        else:
            self.power = 0

    def retract_extender(self):
        #self.power = -1 * power
        self.positionMode = True
        self.target_position = 0

    def isNothingToDig(self):
        if (self.isDistanceReached(40) and  self.digging != 'Nothing' and self.digging == 'Gravel'):
            self.sd.putBoolean("MoveBackwardToDig",True)
            return True
        return False

    def meterToTicks(self, meters):
         
        ticks = meters / (math.pi * SHALF_DIAMETER)  * ENCODER_ROTATION * GEAR_RATIO
        #print("ticks calculated: ",ticks)
        return ticks

    def ticksToMeter(self, ticks):
        #ticks = self.extender_motor.getSelectedSensorPosition(0)
        meters = ticks * (math.pi * SHALF_DIAMETER) /  (ENCODER_ROTATION * GEAR_RATIO)
        return meters

    ''' this is for teleop'''    
    def run(self, power):
        self.power = power

    def execute(self):
        '''This gets called at the end of the control loop'''
        if (self.positionMode):
            self.extender_motor.set(ctre.WPI_TalonSRX.ControlMode.Position,self.target_position)
        else:              
            self.extender_motor.set(ctre.WPI_TalonSRX.ControlMode.PercentOutput,self.power)
        
        self.enabled = False