from pyfrc.physics import motor_cfgs, tankmodel,drivetrains
from pyfrc.physics.units import units
import math
from pyfrc.physics.visionsim import VisionSim
from networktables.util import ntproperty


class PhysicsEngine(object):
    """
        Your physics module must contain a class called ``PhysicsEngine``,
        and it must implement the same functions as this class.
        
        Alternatively, you can inherit from this object. However, that is
        not required.
    """
    target = ntproperty("/camera/target", (0.0, float("inf"), 0.0))

    def __init__(self, physics_controller):
        """
            The constructor must take the following arguments:
            
            :param physics_controller: The physics controller interface
            :type  physics_controller: :class:`.PhysicsInterface`
        """
        self.physics_controller = physics_controller
        self.position = 0

        self.physics_controller.add_device_gyro_channel("navxmxp_spi_4_angle")
        # Change these parameters to fit your robot!
        bumper_width = 3.25 * units.inch

        #self.drivetrain = drivetrains.TwoMotorDrivetrain()
        
        self.drivetrain = tankmodel.TankModel.theory(
            motor_cfgs.MOTOR_CFG_CIM,           # motor configuration
            110 * units.lbs,                    # robot mass
            10.71,                              # drivetrain gear ratio
            2,                                  # motors per side
            22 * units.inch,                    # robot wheelbase
            23 * units.inch + bumper_width * 2, # robot width
            32 * units.inch + bumper_width * 2, # robot length
            6 * units.inch,                     # wheel diameter
        )

        # Precompute the encoder constant
        # -> encoder counts per revolution / wheel circumference
        self.kEncoder = 360 / (0.5 * math.pi)
        
        self.l_distance = 0
        self.r_distance = 0
        targets = [
            # right
            VisionSim.Target(15, 13, 250, 0),
            # middle
            VisionSim.Target(16.5, 15.5, 295, 65),
            # left
            VisionSim.Target(15, 18, 0, 110),
            VisionSim.Target(10, 25, 0, 110),
        ]
        self.vision = VisionSim(
            targets, 61.0, 1.5,20, 15, physics_controller=physics_controller
        )


    def initialize(self, hal_data):
        """
            Called with the hal_data dictionary before the robot has started
            running. Some values may be overwritten when devices are
            initialized... it's not consistent yet, sorry.
        """
        pass


    def update_sim(self, hal_data, now, tm_diff):
        """
            Called when the simulation parameters for the program need to be
            updated. This is mostly when ``wpilib.Timer.delay()`` is called.
            
            :param hal_data: A giant dictionary that has all data about the robot. See
                             ``hal-sim/hal_impl/data.py`` in robotpy-wpilib's repository
                             for more information on the contents of this dictionary.
            :param now: The current time
            :type  now: float
            :param tm_diff: The amount of time that has passed since the last
                            time that this function was called
            :type  tm_diff: float
        """
        # Simulate the drivetrain
        l_motor = hal_data["CAN"][1]["value"]
        # lr_motor = hal_data['pwm'][3]['value']
        r_motor = hal_data["CAN"][2]["value"]
        # rr_motor = hal_data['pwm'][0]['value']

        x, y, angle = self.drivetrain.get_distance(l_motor, r_motor, tm_diff)
        self.physics_controller.distance_drive(x, y, angle)
        
        data = self.vision.compute(now, x, y, angle)
        if data is not None:
            self.target = data[0][:4]
            print("data: ",data)
            print("target: ",self.target)
        ##speed, rotation = self.drivetrain.get_vector(l_motor, r_motor)
        #self.physics_controller.drive(speed, rotation, tm_diff)
        
        #x, y, angle = self.physics_controller.get_position()
        #self.physics_controller.distance_drive(x, y, angle)
        # Update encoders
        '''self.l_distance += self.drivetrain.l_velocity * tm_diff
        self.r_distance += self.drivetrain.r_velocity * tm_diff
        
        hal_data['encoder'][1]['count'] = int(self.l_distance * self.kEncoder)
        hal_data['encoder'][2]['count'] = int(self.r_distance * self.kEncoder)'''
