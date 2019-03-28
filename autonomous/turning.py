from magicbot import AutonomousStateMachine, timed_state, state
# this is one of your components
from components.drive import Drive
from components.scoop import Scoop
from components.depth import Depth
from components.dump import Dump

class DriveForward(AutonomousStateMachine):
    MODE_NAME = 'Turning'
    DEFAULT = False

    # Injected from the definition in robot.py
    drive: Drive
    
    
    @timed_state(duration=1, next_state='drive_backwards')
    def drive_forward(self):
       #self.drive.return_gyro_angle
       self.drive.drive_forward(1)
       
    @timed_state(duration=1, next_state='rotate_90')
    def drive_backwards(self):
       #self.drive.return_gyro_angle
       self.drive.drive_forward(-1)
    
    @state(first=True)
    def rotate_90(self):
        self.drive.rotate(45)
#            self.next_state('drive_stop')

    @timed_state(duration=1)
    def drive_stop(self):
       self.drive.drive_forward(1)
