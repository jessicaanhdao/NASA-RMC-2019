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
    @state(first = True)
    def testServo(self):
        self.servo.reset()
        self.servo.findGoal()

    @timed_state(duration=2)
    def stop(self):
       self.drive.stop()

    @timed_state(duration=3)
    def drive_forward(self):
       self.drive.drive(1)
       
