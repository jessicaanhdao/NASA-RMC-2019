from magicbot import AutonomousStateMachine, tunable, timed_state, state
# this is one of your components
from components.drive import Drive
from components.camera import Camera

class Localize(AutonomousStateMachine):
    MODE_NAME = 'Localize'
    DEFAULT = True

    # Injected from the definition in robot.py
    drive: Drive

    @state(first = True)
    def rotate_360(self):
        self.drive.rotate(90)
        if(self.drive.isGoalFound()):
            print("Found goal")
            self.next_state('stop')
        if (self.drive.isDoneRotation() and not self.drive.isGoalFound()):
            self.drive.reset_gyro_angle()
            self.next_state('rotate_360')
            #self.drive.rotate(90)
            '''if(self.drive.isGoalFound()):
                print("Found goal")
                self.next_state('stop')'''

    @timed_state(duration=2)
    def stop(self):
       self.drive.stop()

    @timed_state(duration=3)
    def drive_forward(self):
       #self.drive.return_gyro_angle
       self.drive.drive_forward(1)
       
