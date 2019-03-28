from magicbot import AutonomousStateMachine, tunable, timed_state, state
# this is one of your components
from components.drive import Drive
class DriveDistance(AutonomousStateMachine):
    MODE_NAME = 'Drive Distance'
    DEFAULT = True

    # Injected from the definition in robot.py
    drive: Drive

    @state(first=True)
    def drive_2m(self):
        self.drive.drive_distance(20)
