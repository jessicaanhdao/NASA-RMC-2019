from magicbot import AutonomousStateMachine, tunable, timed_state, state
# this is one of your components
from components.scoop import Scoop
class Localize(AutonomousStateMachine):
    MODE_NAME = 'Write CSV'
    DEFAULT = False

    # Injected from the definition in robot.py
    scoop: Scoop
    @timed_state(duration = 20, first = True)
    def testServo(self):
        self.scoop.write_CSV()
