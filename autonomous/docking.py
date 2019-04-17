from magicbot import AutonomousStateMachine, tunable, timed_state, state
# this is one of your components
from components.bumpswitch import BumpSwitch
class DriveDistance(AutonomousStateMachine):
    MODE_NAME = 'Docking'
    DEFAULT = False

    # Injected from the definition in robot.py
    bumpswitch: BumpSwitch

    @state(first=True)
    def test(self):
        self.bumpswitch.update()
