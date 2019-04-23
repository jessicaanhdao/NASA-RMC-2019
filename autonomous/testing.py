from magicbot import AutonomousStateMachine, timed_state, state
import wpilib
# these are your components
from components.drive import Drive
from components.scoop import Scoop
from components.extender import Extender
from components.dump import Dump
from components.cameraservo import CameraServo

TIME_LIMIT = 600 #600 seconds = 10 minutes
TIME_DUMP = 60 #1 minute
TIME_RETRACT = 10 #10sec
TIME_DOCK = 10 #10sec


class TestFullBehaviors(AutonomousStateMachine):
    MODE_NAME = 'Test Full Behaviors'
    DEFAULT = True

    # Injected from the definition in robot.py
    drive: Drive
    scoop: Scoop
    extender: Extender
    dump : Dump
    servo : CameraServo

    
    timer = wpilib.Timer()
    timer.reset()
    timer.start()

    TIME_DRIVE = 0 #will be updated
    DRIVE_START = 0
    DRIVE_END = 0

    def isTimeOut(self):
        if (TIME_LIMIT - self.timer.get() < (self.TIME_DRIVE + TIME_RETRACT + TIME_DOCK + TIME_DUMP)):
            return True
        return False
    
    @state()
    def findGoal(self):
        self.timer.reset()
        self.servo.findGoal()
        if (self.drive.isGoalFound()):
            self.next_state = 'localization'
        
    @state(first=True )
    def localization(self):
        if(self.timer.get() >= 600):
            self.done()

        self.drive.rotate2Parallel()
        if (self.drive.isDoneRotating()):
            self.drive.stop()
            self.servo.reset()
            self.drive.resetNavx()
            self.drive.resetEncoder()
            self.DRIVE_START = self.timer.get()
            self.next_state('drive_distance')

    @timed_state(duration=10)
    def drive_distance(self):
        self.drive.drive(1)


    @state()
    def drive_to_mining(self):
        if(self.timer.get() >= 600):
            self.done()

        self.drive.drive_distance(8)
        if (self.drive.isDistanceReached(8)):
            self.DRIVE_END = self.timer.get()
            self.TIME_DRIVE = self.DRIVE_END - self.DRIVE_START
            self.drive.stop()
            self.next_state='digging'

    @state()
    def extending_digger(self):
        if(self.timer.get() >= 600):
            self.done()

        self.extender.extend_distance(0.1)
        if (self.extender.isDistanceReached(0.1)):
            self.extender.extend_down(0) #stop motor before moving on
            self.next_state = 'digging'


    #TODO fix power'''
    @state()
    def digging(self):
       self.scoop.scoop_down(1)
       self.extender.extend_down(0.2)
       if (self.isTimeOut()):
            self.next_state = 'retract_extender'
       if (self.extender.isNothingToDig()):
           self.next_state = 'digging_backwards'
       
    @state()
    def digging_backwards(self):
        self.drive.drive(-0.1)
        self.scoop.scoop_down(1)
        if (self.isTimeOut()):
            self.next_state = 'retract_extender'

    #TODO: check the length of extender to fully know it done extending
    @state( )
    def retract_extender(self):
        self.extender.retract_extender()
        if(self.extender.isDistanceReached(0)):
            self.next_state('drive_back')
        

    @state()
    def drive_back(self):
        '''test drive backwards with encoders'''
        self.drive.drive_distance(0)
        if(self.servo.isGoalInSight() or self.drive.isDistanceReached(0)):
            self.drive.stop()
            self.next_state = "turn_perpendicular"

    @state()
    def turn_perpendicular(self):
        self.drive.rotate2Perpendicular()
        if (self.drive.isDoneRotating()):
            self.drive.stop()
            self.next_state = "docking"

    @state()
    def docking(self):
        self.drive.dock()
        if (self.dump.is_ready()):
            self.next_state('start_dumping')

    #TODO Timing
    @timed_state(duration=TIME_DUMP)
    def start_dumping(self):
        self.dump.start_dumping()
        if(self.timer.get() >= 600):
            self.done()
        else:
            self.drive.rotate(90) 
            self.next_state = 'FindGoal'


    #check time, if still have time, run while loop
