from magicbot import AutonomousStateMachine, tunable, timed_state, state
# this is one of your components
from components.scoop import Scoop
class DriveDistance(AutonomousStateMachine):
    MODE_NAME = 'Scooping'
    DEFAULT = False

    # Injected from the definition in robot.py
    scoop: Scoop

    @state(first=True)
    def test(self):
        self.scoop.write_CSV()
