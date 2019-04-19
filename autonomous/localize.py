from magicbot import AutonomousStateMachine, tunable, timed_state, state
# this is one of your components
from components.drive import Drive
from components.cameraservo import CameraServo
class Localize(AutonomousStateMachine):
    MODE_NAME = 'Localize'
    DEFAULT = False

    # Injected from the definition in robot.py
    drive: Drive
    servo : CameraServo

    @timed_state(duration = 2, first = True, next_state='findGoal')
    def reset(self):
        self.servo.reset()
    @state
    def findGoal(self):
        #self.servo.reset()
        self.servo.findGoal()
