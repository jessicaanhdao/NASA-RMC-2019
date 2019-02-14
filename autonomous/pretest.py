<<<<<<< HEAD
from magicbot import AutonomousStateMachine, tunable, timed_state, state
# this is one of your components
from components.drive import Drive
from components.scoop import Scoop
from components.depth import Depth
from components.dump import Dump

class DriveForward(AutonomousStateMachine):
    MODE_NAME = 'Full Behaviors'
    DEFAULT = True

    # Injected from the definition in robot.py
    drive: Drive
    scoop: Scoop
    depth: Depth
    dump : Dump

    @timed_state(duration=0.5, next_state='drive_forward')
    def drive_wait(self):
        pass

    @timed_state(first=True,duration=1, next_state='drive_backwards')
    def drive_forward(self):
       #self.drive.return_gyro_angle
       self.drive.drive_forward(1)
       
    @timed_state(duration=1, next_state='rotate_90')
    def drive_backwards(self):
       #self.drive.return_gyro_angle
       self.drive.drive_forward(-1)
    
    @timed_state(duration=5, next_state='scoop_down')
    def extend_down(self):
       self.depth.extend_down

    @timed_state(duration=5, next_state = "unextend_depth")
    def scoop_down(self):
        self.scoop.scoop_down

    @timed_state(duration=5, next_state = "rotate_90")
    def unextend_depth(self):
        self.depth.unextend_depth

    @state()
    def rotate_90(self):
        if (self.drive.rotate(90)):
            self.next_state('drive_stop')

    @timed_state(duration=1)
    def drive_stop(self):
       self.drive.drive_forward(1)

    @timed_state(duration=5)
    def drive_90_left(self):
      #  self.drive.rotate(90)
        self.drive.drive_forward(1)
      #  self.next_state('rotate_180')

    @state()
    def rotate_180(self):
        self.drive.rotate(180)
        #self.next_state('rotate_270')

    @state()
    def rotate_270(self):
        self.drive.rotate(-90)
       # self.next_state('rotate_270')

    @timed_state(duration=5)
    def start_dumping(self):
        self.dump.start_dumping


    @state
    def turn_left(self):
        self.drive.tankDrive(0,1)
    @state
    def turn_right(self):
        self.drive.tankDrive(1,0)

=======
from magicbot import AutonomousStateMachine, tunable, timed_state, state
# this is one of your components
from components.drive import Drive
from components.scoop import Scoop
from components.depth import Depth
from components.dump import Dump

class DriveForward(AutonomousStateMachine):
    MODE_NAME = 'Full Behaviors'
    DEFAULT = True

    # Injected from the definition in robot.py
    drive: Drive
    scoop: Scoop
    depth: Depth
    dump : Dump

    @timed_state(duration=0.5, next_state='drive_forward')
    def drive_wait(self):
        pass

    @timed_state(duration=1, next_state='rotate_90')
    def drive_forward(self):
       #self.drive.return_gyro_angle
       self.drive.reset_gyro_angle()
       self.drive.drive_forward(1)
       

    @timed_state(duration=5, next_state='scoop_down')
    def extend_down(self):
       self.depth.extend_down

    @timed_state(duration=5, next_state = "unextend_depth")
    def scoop_down(self):
        self.scoop.scoop_down

    @timed_state(duration=5, next_state = "rotate_90")
    def unextend_depth(self):
        self.depth.unextend_depth

    @state(first=True)
    def rotate_90(self):
        self.drive.rotate(90)
      #  self.next_state('drive_90_left')
    @timed_state(duration=5)
    def drive_90_left(self):
      #  self.drive.rotate(90)
        self.drive.drive_forward(1)
      #  self.next_state('rotate_180')

    @state()
    def rotate_180(self):
        self.drive.rotate(180)
        #self.next_state('rotate_270')

    @state()
    def rotate_270(self):
        self.drive.rotate(-90)
       # self.next_state('rotate_270')

    @timed_state(duration=5)
    def start_dumping(self):
        self.dump.start_dumping


    @state
    def turn_left(self):
        self.drive.tankDrive(0,1)
    @state
    def turn_right(self):
        self.drive.tankDrive(1,0)

>>>>>>> remotes/origin/master
