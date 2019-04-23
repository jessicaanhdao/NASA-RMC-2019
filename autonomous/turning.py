from magicbot import AutonomousStateMachine, timed_state, state
# this is one of your components
from components.drive import Drive
from components.scoop import Scoop
from components.extender import Extender
from components.dump import Dump
import wpilib

class DriveForward(AutonomousStateMachine):
    MODE_NAME = 'Turning'
    DEFAULT = True

    # Injected from the definition in robot.py
    drive: Drive
    i = 0
    timer = wpilib.Timer()
    @state()
    def test(self):
       #self.drive.return_gyro_angle
       self.drive.drive(1)
       self.drive.drive(-1)
       self.i=self.i+1

    @timed_state(duration=5,first = True, next_state='drive_backwards')
    def drive_forward(self):
        #self.drive.return_gyro_angle
        self.drive.drive(1)
        ''' if(self.timer.hasPeriodPassed(50)):
          #self.next_state('drive_backwards')
          self.done()'''
       
    @timed_state(duration=10,next_state='rotate_90')
    def drive_backwards(self):
      #self.drive.return_gyro_angle
      self.drive.drive(-1)
      
    
    @state()
    def rotate_90(self):
        self.drive.rotate(45)
        if (self.drive.isDoneRotating()):
          self.next_state='drive_stop'
            

    @timed_state(duration=5)
    def drive_stop(self):
       self.drive.drive(0)
       self.done(0)
       
